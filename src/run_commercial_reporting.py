from __future__ import annotations

import logging
import time
from pathlib import Path

import pandas as pd

from src.adventureworks.connection import create_database_engine
from src.adventureworks.extract import (
    extract_commercial_data,
    extract_current_product_costs,
    extract_historical_costs,
    extract_sales_detail,
)
from src.adventureworks.transform import calculate_commercial_metrics
from src.generate_adventureworks_report import (
    build_report_data,
    validate_financial_calculations,
)
from src.adventureworks.datasets import build_reporting_datasets
from src.maven_crm.datasets import (
    build_account_performance,
    build_executive_pipeline_kpis,
    build_product_performance,
    build_regional_performance,
    build_sales_agent_performance,
    build_stage_performance,
)
from src.maven_crm.extract import (
    extract_accounts,
    extract_products,
    extract_sales_pipeline,
    extract_sales_teams,
)
from src.maven_crm.transform import (
    derive_pipeline_business_state,
    derive_pipeline_value_metrics,
    enrich_account_information,
    enrich_sales_team_information,
    standardize_product_names,
)
from src.maven_crm.validate import validate_maven_data
from src.reporting.recommendations import build_management_recommendations


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTING_DIRECTORY = PROJECT_ROOT / "data" / "reporting"
LOG_DIRECTORY = PROJECT_ROOT / "logs"

logger = logging.getLogger("commercial_reporting")


def configure_logging() -> None:
    """Configure console and persistent file logging for scheduled runs."""
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_DIRECTORY / "commercial_reporting.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def export_csv(dataframe: pd.DataFrame, filename: str) -> Path:
    """Write one prepared reporting dataset to the Power BI reporting layer."""
    REPORTING_DIRECTORY.mkdir(parents=True, exist_ok=True)

    output_path = REPORTING_DIRECTORY / filename
    dataframe.to_csv(output_path, index=False)

    logger.info(
        "Exported %s (%s rows)",
        output_path,
        len(dataframe),
    )

    return output_path


def build_adventureworks_outputs() -> dict:
    """
    Extract, calculate, validate, and export AdventureWorks reporting data.

    This is the reporting layer used by the Power BI actual-performance pages.
    """
    logger.info("Starting AdventureWorks reporting pipeline")

    engine = create_database_engine()

    sales_detail_df = extract_sales_detail(engine)
    commercial_data_df = extract_commercial_data(engine)
    historical_cost_df = extract_historical_costs(engine)
    current_cost_df = extract_current_product_costs(engine)

    if sales_detail_df.empty:
        raise ValueError(
            "AdventureWorks sales extraction returned zero rows."
        )

    reporting_df = calculate_commercial_metrics(
        commercial_data_df,
        historical_cost_df,
        current_cost_df,
    )

    if len(reporting_df) != len(sales_detail_df):
        raise ValueError(
            "AdventureWorks reporting population does not match "
            "the extracted sales population."
        )

    if reporting_df["SalesOrderDetailID"].isna().any():
        raise ValueError(
            "AdventureWorks SalesOrderDetailID contains nulls."
        )

    if not reporting_df["SalesOrderDetailID"].is_unique:
        raise ValueError(
            "AdventureWorks SalesOrderDetailID is not unique "
            "at sales-line grain."
        )

    if reporting_df["Revenue"].isna().any():
        raise ValueError(
            "AdventureWorks Revenue contains nulls."
        )

    if (reporting_df["Revenue"] < 0).any():
        raise ValueError(
            "AdventureWorks contains negative Revenue values."
        )

    validate_financial_calculations(reporting_df)

    # Preserve the legacy report data contract for recommendations.
    report_data = build_report_data(reporting_df)

    # Build the established Power BI reporting datasets.
    reporting_datasets = build_reporting_datasets(reporting_df)

    dataset_files = {
        "executive_kpis": "executive_kpis.csv",
        "monthly_performance": "monthly_performance.csv",
        "category_performance": "category_performance.csv",
        "product_performance": "product_performance.csv",
        "customer_performance": "customer_performance.csv",
        "seller_performance": "seller_performance.csv",
        "key_observations": "key_observations.csv",
    }

    for dataset_name, filename in dataset_files.items():
        dataset = reporting_datasets[dataset_name]

        if isinstance(dataset, list):
            dataframe = pd.DataFrame(dataset)
        else:
            dataframe = dataset.copy()

        if "OrderMonth" in dataframe.columns:
            dataframe["OrderMonth"] = (
                dataframe["OrderMonth"].astype(str)
            )

        export_csv(dataframe, filename)

    logger.info(
        "AdventureWorks reporting datasets exported successfully"
    )

    return report_data


def build_maven_outputs() -> dict:
    """
    Extract, validate, transform, aggregate, and export Maven CRM data.
    """
    logger.info("Starting Maven CRM reporting pipeline")

    sales_pipeline_df = extract_sales_pipeline()
    accounts_df = extract_accounts()
    products_df = extract_products()
    sales_teams_df = extract_sales_teams()

    # Normalize known source naming differences before relational validation.
    # The source uses "GTXPro", while the product master uses "GTX Pro".
    # This is a controlled business-standardization step, not a source-file edit.
    standardized_pipeline_df = standardize_product_names(
        sales_pipeline_df
    )

    changed_product_rows = (
        sales_pipeline_df["product"].fillna("")
        != standardized_pipeline_df["product_standardized"].fillna("")
    ).sum()

    if changed_product_rows:
        logger.warning(
            "Maven product normalization applied to %s rows before validation.",
            changed_product_rows,
        )

    # Create a validation copy so the raw source dataframe remains unchanged.
    # The Maven validator expects the product field to match the product master.
    validation_pipeline_df = sales_pipeline_df.copy()

    validation_pipeline_df["product"] = (
        standardized_pipeline_df["product_standardized"]
    )

    validate_maven_data(
        validation_pipeline_df,
        accounts_df,
        products_df,
        sales_teams_df,
    )

    transformed_pipeline_df = standardized_pipeline_df
    transformed_pipeline_df = enrich_sales_team_information(
        transformed_pipeline_df,
        sales_teams_df,
    )
    transformed_pipeline_df = enrich_account_information(
        transformed_pipeline_df,
        accounts_df,
    )
    transformed_pipeline_df = derive_pipeline_business_state(
        transformed_pipeline_df
    )
    transformed_pipeline_df = derive_pipeline_value_metrics(
        transformed_pipeline_df
    )

    datasets = {
        "executive_pipeline_kpis": build_executive_pipeline_kpis(
            transformed_pipeline_df
        ),
        "stage_performance": build_stage_performance(
            transformed_pipeline_df
        ),
        "regional_performance": build_regional_performance(
            transformed_pipeline_df
        ),
        "sales_agent_performance": build_sales_agent_performance(
            transformed_pipeline_df
        ),
        "product_performance": build_product_performance(
            transformed_pipeline_df
        ),
        "account_performance": build_account_performance(
            transformed_pipeline_df,
            accounts_df,
        ),
    }

    for dataset_name, dataframe in datasets.items():
        export_csv(
            dataframe,
            f"maven_crm/{dataset_name}.csv",
        )

    logger.info(
        "Maven CRM reporting complete: %s opportunities",
        len(transformed_pipeline_df),
    )

    return {
        "transformed_pipeline": transformed_pipeline_df,
        **datasets,
    }


def build_management_recommendation_output(
    adventureworks: dict,
    maven: dict,
) -> pd.DataFrame:
    """Build and validate the five management recommendations."""
    recommendations_df = build_management_recommendations(
        executive_kpis=adventureworks["executive"],
        category_df=adventureworks["category"],
        adventureworks_product_df=adventureworks["product"],
        customer_df=adventureworks["customer"],
        seller_df=adventureworks["seller"],
        transformed_pipeline_df=maven["transformed_pipeline"],
        regional_df=maven["regional_performance"],
        maven_product_df=maven["product_performance"],
    )

    if len(recommendations_df) != 5:
        raise ValueError(
            "Expected 5 management recommendations, "
            f"received {len(recommendations_df)}."
        )

    expected_ids = [1, 2, 3, 4, 5]
    actual_ids = recommendations_df["RecommendationID"].tolist()

    if actual_ids != expected_ids:
        raise ValueError(
            "Recommendation IDs are not sequential: "
            f"{actual_ids}"
        )

    required_columns = [
        "RecommendationID",
        "Priority",
        "Area",
        "Finding",
        "Recommendation",
        "Metric",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in recommendations_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Management recommendation output is missing columns: "
            f"{missing_columns}"
        )

    if recommendations_df[required_columns].isna().any().any():
        raise ValueError(
            "Management recommendation output contains null values."
        )

    export_csv(
        recommendations_df[required_columns],
        "management_recommendations.csv",
    )

    logger.info("Management recommendation output complete: 5 rows")

    return recommendations_df


def run_pipeline() -> None:
    """Run the complete Python reporting pipeline."""
    configure_logging()

    start_time = time.perf_counter()

    logger.info("=" * 70)
    logger.info("AUTOMATED COMMERCIAL PERFORMANCE REPORTING SYSTEM")
    logger.info("PIPELINE START")
    logger.info("=" * 70)

    try:
        adventureworks = build_adventureworks_outputs()
        maven = build_maven_outputs()

        build_management_recommendation_output(
            adventureworks,
            maven,
        )

        elapsed_seconds = time.perf_counter() - start_time

        logger.info("=" * 70)
        logger.info("PIPELINE COMPLETE")
        logger.info("Status: PASS")
        logger.info(
            "Elapsed time: %.2f seconds",
            elapsed_seconds,
        )
        logger.info(
            "Reporting outputs are ready for Power BI refresh."
        )
        logger.info("=" * 70)

    except Exception:
        logger.exception("PIPELINE FAILED")
        raise


if __name__ == "__main__":
    run_pipeline()

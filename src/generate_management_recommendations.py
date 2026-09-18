from pathlib import Path

from src.adventureworks.connection import create_database_engine
from src.adventureworks.extract import (
    extract_commercial_data,
    extract_current_product_costs,
    extract_historical_costs,
    extract_sales_detail,
)
from src.adventureworks.transform import calculate_commercial_metrics
from src.reporting.recommendations import (
    build_management_recommendations,
    export_management_recommendations_with_summary,
)
from src.generate_adventureworks_report import build_report_data
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
from src.maven_crm.datasets import (
    build_product_performance,
    build_regional_performance,
)


DEFAULT_OUTPUT_DIRECTORY = Path("data/reporting")


def build_adventureworks_reporting_data():
    """
    Reuse the existing AdventureWorks extraction, calculation,
    and reporting-dataset pipeline.

    This function does not create a second AdventureWorks logic path.
    It calls the same functions already used by the reporting script.
    """
    print()
    print("ADVENTUREWORKS REPORTING DATA")
    print("=" * 60)

    engine = create_database_engine()

    sales_detail_df = extract_sales_detail(engine)
    commercial_data_df = extract_commercial_data(engine)
    historical_cost_df = extract_historical_costs(engine)
    current_cost_df = extract_current_product_costs(engine)

    reporting_df = calculate_commercial_metrics(
        commercial_data_df,
        historical_cost_df,
        current_cost_df,
    )

    report_data = build_report_data(reporting_df)

    print(f"Sales detail rows: {len(sales_detail_df):,}")
    print(f"Reporting rows: {len(reporting_df):,}")
    print(f"Category rows: {len(report_data['category']):,}")
    print(f"Product rows: {len(report_data['product']):,}")
    print(f"Customer rows: {len(report_data['customer']):,}")
    print(f"Seller rows: {len(report_data['seller']):,}")

    return report_data


def build_maven_reporting_data():
    """
    Reuse the existing Maven CRM extraction and transformation functions
    to create the reporting datasets required by the recommendation engine.
    """
    print()
    print("MAVEN CRM REPORTING DATA")
    print("=" * 60)

    sales_pipeline_df = extract_sales_pipeline()
    accounts_df = extract_accounts()
    products_df = extract_products()
    sales_teams_df = extract_sales_teams()

    transformed_pipeline_df = standardize_product_names(
        sales_pipeline_df
    )

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

    regional_df = build_regional_performance(
        transformed_pipeline_df
    )

    product_df = build_product_performance(
        transformed_pipeline_df
    )

    print(f"Pipeline rows: {len(transformed_pipeline_df):,}")
    print(f"Regional rows: {len(regional_df):,}")
    print(f"Product rows: {len(product_df):,}")

    return {
        "transformed_pipeline": transformed_pipeline_df,
        "regional": regional_df,
        "product": product_df,
    }


def generate_management_recommendations():
    """
    Build management recommendations from the actual reporting datasets
    produced by both source pipelines.
    """
    adventureworks = build_adventureworks_reporting_data()
    maven = build_maven_reporting_data()

    recommendations_df = build_management_recommendations(
        executive_kpis=adventureworks["executive"],
        category_df=adventureworks["category"],
        adventureworks_product_df=adventureworks["product"],
        customer_df=adventureworks["customer"],
        seller_df=adventureworks["seller"],
        transformed_pipeline_df=maven["transformed_pipeline"],
        regional_df=maven["regional"],
        maven_product_df=maven["product"],
    )

    output_path = export_management_recommendations_with_summary(
        recommendations_df,
        output_directory=DEFAULT_OUTPUT_DIRECTORY,
    )

    print()
    print("REAL-DATA INTEGRATION")
    print("=" * 60)
    print("Recommendation rows:", len(recommendations_df))
    print("Output:", output_path)
    print("REAL-DATA INTEGRATION: PASS")

    return recommendations_df


if __name__ == "__main__":
    generate_management_recommendations()

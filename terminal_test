from src.maven_crm.extract import (
    extract_accounts,
    extract_products,
    extract_sales_pipeline,
    extract_sales_teams,
)

from src.maven_crm.transform import (
    standardize_product_names,
    enrich_sales_team_information,
    enrich_account_information,
    derive_pipeline_business_state,
    derive_pipeline_value_metrics,
)

from src.maven_crm.datasets import (
    build_executive_pipeline_kpis,
    build_stage_performance,
    build_regional_performance,
    build_sales_agent_performance,
    build_product_performance,
    build_account_performance,
)

from src.maven_crm.export import (
    export_maven_reporting_datasets_with_summary,
)


def main():

    print("Extracting Maven CRM data...")

    sales_pipeline_df = extract_sales_pipeline()
    accounts_df = extract_accounts()
    products_df = extract_products()
    sales_teams_df = extract_sales_teams()

    print("Extraction completed.")
    print()

    print("Applying transformations...")

    transformed_df = standardize_product_names(
        sales_pipeline_df
    )

    transformed_df = enrich_sales_team_information(
        transformed_df,
        sales_teams_df,
    )

    transformed_df = enrich_account_information(
        transformed_df,
        accounts_df,
    )

    transformed_df = derive_pipeline_business_state(
        transformed_df
    )

    transformed_df = derive_pipeline_value_metrics(
        transformed_df
    )

    print("Transformation completed.")
    print()

    print("Building reporting datasets...")

    executive_pipeline_kpis = (
        build_executive_pipeline_kpis(
            transformed_df
        )
    )

    stage_performance = (
        build_stage_performance(
            transformed_df
        )
    )

    regional_performance = (
        build_regional_performance(
            transformed_df
        )
    )

    sales_agent_performance = (
        build_sales_agent_performance(
            transformed_df
        )
    )

    product_performance = (
        build_product_performance(
            transformed_df
        )
    )

    account_performance = (
        build_account_performance(
            transformed_df,
            accounts_df,
        )
    )

    print("Reporting datasets completed.")
    print()

    maven_reporting_datasets = {
        "executive_pipeline_kpis":
            executive_pipeline_kpis,
        "stage_performance":
            stage_performance,
        "regional_performance":
            regional_performance,
        "sales_agent_performance":
            sales_agent_performance,
        "product_performance":
            product_performance,
        "account_performance":
            account_performance,
    }

    export_maven_reporting_datasets_with_summary(
        maven_reporting_datasets
    )


if __name__ == "__main__":
    main()
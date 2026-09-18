from src.maven_crm.extract import (
    extract_accounts,
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


def main():
    print("Extracting Maven CRM data...")

    sales_pipeline_df = extract_sales_pipeline()
    sales_teams_df = extract_sales_teams()
    accounts_df = extract_accounts()

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

    print("Building executive pipeline KPIs...")

    executive_kpis = build_executive_pipeline_kpis(
        transformed_df
    )

    print()
    print("EXECUTIVE PIPELINE KPIs")
    print("=" * 60)

    print(
        executive_kpis.to_string(index=False)
    )

    print()
    print("Dataset shape:")
    print(executive_kpis.shape)

    print()
    print("Dataset columns:")
    print(
        list(executive_kpis.columns)
    )

    print()
    print("Building stage performance dataset...")

    stage_performance = build_stage_performance(
        transformed_df
    )

    print()
    print("STAGE PERFORMANCE")
    print("=" * 60)

    print(
        stage_performance.to_string(index=False)
    )

    print()
    print("Dataset shape:")
    print(stage_performance.shape)

    print()
    print("Stage opportunity total:")
    print(
        stage_performance["OpportunityCount"].sum()
    )

    print()
    print("Stage share total:")
    print(
        round(
            stage_performance[
                "OpportunitySharePct"
            ].sum(),
            4,
        )
    )

    print()
    print("Won opportunity total:")
    print(
        stage_performance["WonCount"].sum()
    )

    print()
    print("Lost opportunity total:")
    print(
        stage_performance["LostCount"].sum()
    )

    print()
    print("Building regional performance dataset...")

    regional_performance = build_regional_performance(
        transformed_df
    )

    print()
    print("REGIONAL PERFORMANCE")
    print("=" * 60)

    print(
        regional_performance.to_string(index=False)
    )

    print()
    print("Dataset shape:")
    print(regional_performance.shape)

    print()
    print("Regional opportunity total:")
    print(
        regional_performance[
            "OpportunityCount"
        ].sum()
    )

    print()
    print("Regional share total:")
    print(
        round(
            regional_performance[
                "OpportunitySharePct"
            ].sum(),
            4,
        )
    )

    print()
    print("Regional won total:")
    print(
        regional_performance[
            "WonCount"
        ].sum()
    )

    print()
    print("Regional lost total:")
    print(
        regional_performance[
            "LostCount"
        ].sum()
    )

    print()
    print("Building sales agent performance dataset...")

    sales_agent_performance = build_sales_agent_performance(
        transformed_df
    )

    print()
    print("SALES AGENT PERFORMANCE")
    print("=" * 60)

    print(
        sales_agent_performance.to_string(index=False)
    )

    print()
    print("Dataset shape:")
    print(sales_agent_performance.shape)

    print()
    print("Sales agent opportunity total:")
    print(
        sales_agent_performance[
            "OpportunityCount"
        ].sum()
    )

    print()
    print("Sales agent share total:")
    print(
        round(
            sales_agent_performance[
                "OpportunitySharePct"
            ].sum(),
            4,
        )
    )

    print()
    print("Sales agent won total:")
    print(
        sales_agent_performance[
            "WonCount"
        ].sum()
    )

    print()
    print("Sales agent lost total:")
    print(
        sales_agent_performance[
            "LostCount"
        ].sum()
    )

    print()
    print("Unique sales agents:")
    print(
        sales_agent_performance[
            "sales_agent"
        ].nunique()
    )

    print()
    print("Building product performance dataset...")

    product_performance = build_product_performance(
        transformed_df
    )

    print()
    print("PRODUCT PERFORMANCE")
    print("=" * 60)

    print(
        product_performance.to_string(index=False)
    )

    print()
    print("Dataset shape:")
    print(product_performance.shape)

    print()
    print("Product opportunity total:")
    print(
        product_performance[
            "OpportunityCount"
        ].sum()
    )

    print()
    print("Product share total:")
    print(
        round(
            product_performance[
                "OpportunitySharePct"
            ].sum(),
            4,
        )
    )

    print()
    print("Product won total:")
    print(
        product_performance[
            "WonCount"
        ].sum()
    )

    print()
    print("Product lost total:")
    print(
        product_performance[
            "LostCount"
        ].sum()
    )

    print()
    print("Unique standardized products:")
    print(
        product_performance[
            "product_standardized"
        ].nunique()
    )

    print()
    print("Building account performance dataset...")

    account_performance = build_account_performance(
        transformed_df,
        accounts_df,
    )

    print()
    print("ACCOUNT PERFORMANCE")
    print("=" * 60)

    print(
        account_performance.to_string(index=False)
    )

    print()
    print("Dataset shape:")
    print(account_performance.shape)

    print()
    print("Account opportunity total:")
    print(
        account_performance[
            "OpportunityCount"
        ].sum()
    )

    print()
    print("Account share total:")
    print(
        round(
            account_performance[
                "OpportunitySharePct"
            ].sum(),
            4,
        )
    )

    print()
    print("Account won total:")
    print(
        account_performance[
            "WonCount"
        ].sum()
    )

    print()
    print("Account lost total:")
    print(
        account_performance[
            "LostCount"
        ].sum()
    )

    print()
    print("Unique accounts:")
    print(
        account_performance[
            "account"
        ].nunique()
    )

    
if __name__ == "__main__":
    main()
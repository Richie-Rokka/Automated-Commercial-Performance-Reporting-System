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


def main():
    print("Extracting Maven CRM data...")

    sales_pipeline_df = extract_sales_pipeline()
    sales_teams_df = extract_sales_teams()
    accounts_df = extract_accounts()

    print("Extraction completed.")
    print()

    # ---------------------------------------------------------
    # Product Standardization
    # ---------------------------------------------------------

    print("Applying product standardization...")

    transformed_df = standardize_product_names(
        sales_pipeline_df
    )

    # ---------------------------------------------------------
    # Sales-Team Enrichment
    # ---------------------------------------------------------

    print("Enriching sales-team information...")

    transformed_df = enrich_sales_team_information(
        transformed_df,
        sales_teams_df,
    )

    # ---------------------------------------------------------
    # Account Enrichment
    # ---------------------------------------------------------

    print("Enriching account information...")

    transformed_df = enrich_account_information(
        transformed_df,
        accounts_df,
    )

    # ---------------------------------------------------------
    # Pipeline Business-State Derivation
    # ---------------------------------------------------------

    print("Deriving pipeline business state...")

    transformed_df = derive_pipeline_business_state(
        transformed_df
    )

    # ---------------------------------------------------------
    # Pipeline Value Metrics
    # ---------------------------------------------------------

    print("Deriving pipeline value metrics...")

    transformed_df = derive_pipeline_value_metrics(
        transformed_df
    )

    # ---------------------------------------------------------
    # Product Standardization Results
    # ---------------------------------------------------------

    print()
    print("PRODUCT STANDARDIZATION")
    print("=" * 60)

    print(
        transformed_df[
            [
                "product",
                "product_standardized",
            ]
        ]
        .drop_duplicates()
        .sort_values("product")
        .to_string(index=False)
    )

    print()

    print(
        "GTXPro standardized rows:",
        (
            transformed_df["product_standardized"]
            == "GTX Pro"
        ).sum(),
    )

    # ---------------------------------------------------------
    # Sales-Team Enrichment Results
    # ---------------------------------------------------------

    print()
    print("SALES TEAM ENRICHMENT")
    print("=" * 60)

    print(
        transformed_df[
            [
                "sales_agent",
                "manager",
                "regional_office",
            ]
        ]
        .drop_duplicates()
        .sort_values("sales_agent")
        .to_string(index=False)
    )

    # ---------------------------------------------------------
    # Account Enrichment Results
    # ---------------------------------------------------------

    print()
    print("ACCOUNT ENRICHMENT")
    print("=" * 60)

    print(
        transformed_df[
            [
                "account",
                "sector",
                "revenue",
                "employees",
                "office_location",
            ]
        ]
        .drop_duplicates()
        .head(10)
        .to_string(index=False)
    )

    # ---------------------------------------------------------
    # Account Enrichment Integrity
    # ---------------------------------------------------------

    print()
    print("ACCOUNT ENRICHMENT INTEGRITY")
    print("=" * 60)

    missing_source_accounts = (
        transformed_df["account"].isna().sum()
    )

    unmatched_accounts = (
        transformed_df["account"].notna()
        & transformed_df["sector"].isna()
    ).sum()

    print(
        "Opportunities with missing source account:",
        missing_source_accounts,
    )

    print(
        "Opportunities with unmatched account:",
        unmatched_accounts,
    )

    print(
        "Missing manager values:",
        transformed_df["manager"].isna().sum(),
    )

    print(
        "Missing regional office values:",
        transformed_df["regional_office"].isna().sum(),
    )

    # ---------------------------------------------------------
    # Pipeline Business-State Results
    # ---------------------------------------------------------

    print()
    print("PIPELINE BUSINESS STATE")
    print("=" * 60)

    print(
        transformed_df[
            [
                "deal_stage",
                "pipeline_status",
                "is_won",
                "is_lost",
            ]
        ]
        .drop_duplicates()
        .sort_values("deal_stage")
        .to_string(index=False)
    )

    print()

    print("Pipeline status counts:")
    print(
        transformed_df["pipeline_status"]
        .value_counts()
        .sort_index()
    )

    print()

    print(
        "Won opportunities:",
        transformed_df["is_won"].sum(),
    )

    print(
        "Lost opportunities:",
        transformed_df["is_lost"].sum(),
    )

    # ---------------------------------------------------------
    # Pipeline Value Metrics
    # ---------------------------------------------------------

    print()
    print("PIPELINE VALUE METRICS")
    print("=" * 60)

    print(
        transformed_df[
            [
                "deal_stage",
                "close_value",
                "pipeline_probability",
                "weighted_close_value",
                "is_open",
                "is_closed",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print()

    total_close_value = (
        transformed_df["close_value"].sum()
    )

    total_weighted_close_value = (
        transformed_df["weighted_close_value"].sum()
    )

    open_opportunities = transformed_df[
        transformed_df["is_open"]
    ]

    closed_opportunities = transformed_df[
        transformed_df["is_closed"]
    ]

    open_close_value_missing = (
        open_opportunities["close_value"]
        .isna()
        .sum()
    )

    open_weighted_value_missing = (
        open_opportunities["weighted_close_value"]
        .isna()
        .sum()
    )

    print(
        "Total Close Value:",
        round(total_close_value, 2),
    )

    print(
        "Total Weighted Close Value:",
        round(total_weighted_close_value, 2),
    )

    print(
        "Open opportunities:",
        len(open_opportunities),
    )

    print(
        "Open opportunities with missing close value:",
        open_close_value_missing,
    )

    print(
        "Open opportunities with missing weighted value:",
        open_weighted_value_missing,
    )

    print(
        "Closed opportunities:",
        len(closed_opportunities),
    )

    # ---------------------------------------------------------
    # Transformation Integrity
    # ---------------------------------------------------------

    print()
    print("TRANSFORMATION INTEGRITY")
    print("=" * 60)

    print(
        "Pipeline rows:",
        len(sales_pipeline_df),
    )

    print(
        "Transformed rows:",
        len(transformed_df),
    )

    print(
        "Missing pipeline status values:",
        transformed_df["pipeline_status"].isna().sum(),
    )

    print(
        "Missing pipeline probability values:",
        transformed_df["pipeline_probability"].isna().sum(),
    )

    print(
        "Won flag count:",
        transformed_df["is_won"].sum(),
    )

    print(
        "Lost flag count:",
        transformed_df["is_lost"].sum(),
    )

    print(
        "Open flag count:",
        transformed_df["is_open"].sum(),
    )

    print(
        "Closed flag count:",
        transformed_df["is_closed"].sum(),
    )


if __name__ == "__main__":
    main()
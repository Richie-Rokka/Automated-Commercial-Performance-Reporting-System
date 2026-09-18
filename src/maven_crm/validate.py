import pandas as pd


def validate_pipeline_population(sales_pipeline_df, expected_row_count=8_800):
    actual_row_count = len(sales_pipeline_df)
    if actual_row_count != expected_row_count:
        raise ValueError(
            f"Pipeline population validation failed. "
            f"Expected {expected_row_count:,} rows, but received {actual_row_count:,}."
        )
    print(f"Pipeline population validation: PASS ({actual_row_count:,} rows)")


def validate_opportunity_id(sales_pipeline_df):
    missing_ids = sales_pipeline_df["opportunity_id"].isna().sum()
    if missing_ids > 0:
        raise ValueError(
            f"Opportunity ID validation failed. "
            f"{missing_ids:,} rows have a missing opportunity_id."
        )

    duplicate_ids = sales_pipeline_df["opportunity_id"].duplicated().sum()
    if duplicate_ids > 0:
        raise ValueError(
            f"Opportunity ID validation failed. "
            f"{duplicate_ids:,} duplicate opportunity IDs found."
        )

    print(f"Opportunity ID validation: PASS ({len(sales_pipeline_df):,} unique IDs)")


def validate_deal_stages(sales_pipeline_df):
    valid_stages = {"Prospecting", "Engaging", "Won", "Lost"}
    actual_stages = set(sales_pipeline_df["deal_stage"].dropna().unique())
    invalid_stages = actual_stages - valid_stages

    if invalid_stages:
        raise ValueError(
            f"Deal stage validation failed. Invalid stages found: {sorted(invalid_stages)}"
        )

    print(f"Deal stage validation: PASS ({len(actual_stages)} valid stages)")


def validate_stage_date_completeness(sales_pipeline_df):
    engage_required = sales_pipeline_df[
        sales_pipeline_df["deal_stage"].isin({"Engaging", "Won", "Lost"})
    ]
    missing_engage_dates = engage_required["engage_date"].isna().sum()

    if missing_engage_dates > 0:
        raise ValueError(
            f"Engage date validation failed. "
            f"{missing_engage_dates:,} Engaging/Won/Lost opportunities have no engage_date."
        )

    close_required = sales_pipeline_df[
        sales_pipeline_df["deal_stage"].isin({"Won", "Lost"})
    ]
    missing_close_dates = close_required["close_date"].isna().sum()

    if missing_close_dates > 0:
        raise ValueError(
            f"Close date validation failed. "
            f"{missing_close_dates:,} Won/Lost opportunities have no close_date."
        )

    print("Stage-based date completeness validation: PASS")


def validate_date_chronology(sales_pipeline_df):
    dated_rows = sales_pipeline_df[
        sales_pipeline_df["engage_date"].notna()
        & sales_pipeline_df["close_date"].notna()
    ]

    invalid_dates = (
        dated_rows["close_date"] < dated_rows["engage_date"]
    ).sum()

    if invalid_dates > 0:
        raise ValueError(
            f"Date chronology validation failed. "
            f"{invalid_dates:,} opportunities have a close_date before engage_date."
        )

    print(
        f"Date chronology validation: PASS "
        f"({len(dated_rows):,} dated opportunities checked)"
    )


def find_unmatched_values(child_df, child_column, parent_df, parent_column):
    child_values = child_df[child_column].dropna().unique()
    parent_values = parent_df[parent_column].dropna().unique()
    return set(child_values) - set(parent_values)


def validate_pipeline_accounts(sales_pipeline_df, accounts_df):
    unmatched_accounts = find_unmatched_values(
        sales_pipeline_df, "account", accounts_df, "account"
    )

    if unmatched_accounts:
        raise ValueError(
            f"Pipeline-to-account validation failed. "
            f"Unmatched accounts: {sorted(unmatched_accounts)}"
        )

    print("Pipeline-to-account validation: PASS")


def validate_pipeline_products(sales_pipeline_df, products_df):
    unmatched_products = find_unmatched_values(
        sales_pipeline_df, "product", products_df, "product"
    )

    if unmatched_products:
        affected_rows = sales_pipeline_df[
            sales_pipeline_df["product"].isin(unmatched_products)
        ]

        print("Pipeline-to-product validation: EXCEPTION")
        print(f"Unmatched product values: {sorted(unmatched_products)}")
        print(f"Affected opportunities: {len(affected_rows):,}")
        return

    print("Pipeline-to-product validation: PASS")


def validate_pipeline_sales_agents(sales_pipeline_df, sales_teams_df):
    unmatched_agents = find_unmatched_values(
        sales_pipeline_df, "sales_agent", sales_teams_df, "sales_agent"
    )

    if unmatched_agents:
        raise ValueError(
            f"Pipeline-to-sales-team validation failed. "
            f"Unmatched sales agents: {sorted(unmatched_agents)}"
        )

    print("Pipeline-to-sales-team validation: PASS")


def validate_account_hierarchy(accounts_df):
    unmatched_parent_accounts = find_unmatched_values(
        accounts_df, "subsidiary_of", accounts_df, "account"
    )

    if unmatched_parent_accounts:
        raise ValueError(
            f"Account hierarchy validation failed. "
            f"Unmatched parent accounts: {sorted(unmatched_parent_accounts)}"
        )

    print("Account hierarchy validation: PASS")


def validate_maven_data(
    sales_pipeline_df,
    accounts_df,
    products_df,
    sales_teams_df,
    expected_row_count=8_800,
):
    print("MAVEN CRM VALIDATION")
    print("=" * 60)

    validate_pipeline_population(sales_pipeline_df, expected_row_count)
    validate_opportunity_id(sales_pipeline_df)
    validate_deal_stages(sales_pipeline_df)
    validate_stage_date_completeness(sales_pipeline_df)
    validate_date_chronology(sales_pipeline_df)
    validate_pipeline_accounts(sales_pipeline_df, accounts_df)
    validate_pipeline_products(sales_pipeline_df, products_df)
    validate_pipeline_sales_agents(sales_pipeline_df, sales_teams_df)
    validate_account_hierarchy(accounts_df)

    print("=" * 60)
    print("Maven CRM validation completed.")

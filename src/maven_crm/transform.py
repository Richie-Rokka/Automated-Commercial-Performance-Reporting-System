import pandas as pd


def standardize_product_names(sales_pipeline_df):
    """
    Standardize known product naming inconsistencies
    while preserving the original source value.
    """

    transformed_df = sales_pipeline_df.copy()

    transformed_df["product_standardized"] = (
        transformed_df["product"]
        .replace({
            "GTXPro": "GTX Pro"
        })
    )

    return transformed_df

def enrich_sales_team_information(
    sales_pipeline_df,
    sales_teams_df,
):
    """
    Add sales manager and regional office
    information to the sales pipeline.
    """

    transformed_df = sales_pipeline_df.copy()

    transformed_df = transformed_df.merge(
        sales_teams_df[
            [
                "sales_agent",
                "manager",
                "regional_office",
            ]
        ],
        on="sales_agent",
        how="left",
    )

    return transformed_df

def enrich_account_information(
    sales_pipeline_df,
    accounts_df,
):
    """
    Add account attributes to the sales pipeline.
    """

    transformed_df = sales_pipeline_df.copy()

    transformed_df = transformed_df.merge(
        accounts_df[
            [
                "account",
                "sector",
                "year_established",
                "revenue",
                "employees",
                "office_location",
                "subsidiary_of",
            ]
        ],
        on="account",
        how="left",
    )

    return transformed_df

def derive_pipeline_business_state(sales_pipeline_df):
    """
    Derive reporting-ready business-state fields
    from the CRM deal stage.
    """

    transformed_df = sales_pipeline_df.copy()

    transformed_df["pipeline_status"] = (
        transformed_df["deal_stage"]
        .map({
            "Prospecting": "Open",
            "Engaging": "Open",
            "Won": "Closed",
            "Lost": "Closed",
        })
    )

    transformed_df["is_won"] = (
        transformed_df["deal_stage"] == "Won"
    )

    transformed_df["is_lost"] = (
        transformed_df["deal_stage"] == "Lost"
    )

    return transformed_df

def derive_pipeline_value_metrics(sales_pipeline_df):
    """
    Derive commercial pipeline value metrics.

    Preserves missing close_value values for open opportunities
    and calculates weighted value only when a close value exists.
    """

    transformed_df = sales_pipeline_df.copy()

    # -------------------------------------------------------
    # Pipeline Probability
    # -------------------------------------------------------

    probability_map = {
        "Prospecting": 0.10,
        "Engaging": 0.60,
        "Won": 1.00,
        "Lost": 0.00,
    }

    transformed_df["pipeline_probability"] = (
        transformed_df["deal_stage"]
        .map(probability_map)
    )

    # -------------------------------------------------------
    # Weighted Close Value
    # -------------------------------------------------------

    transformed_df["weighted_close_value"] = (
        transformed_df["close_value"]
        * transformed_df["pipeline_probability"]
    )

    # -------------------------------------------------------
    # Pipeline State Flags
    # -------------------------------------------------------

    transformed_df["is_open"] = (
        transformed_df["pipeline_status"] == "Open"
    )

    transformed_df["is_closed"] = (
        transformed_df["pipeline_status"] == "Closed"
    )

    return transformed_df
import pandas as pd

def build_executive_pipeline_kpis(transformed_df):
    """
    Build a one-row executive summary of Maven CRM pipeline performance.
    """

    total_opportunities = len(transformed_df)

    open_opportunities = (
        transformed_df["is_open"].sum()
    )

    closed_opportunities = (
        transformed_df["is_closed"].sum()
    )

    won_opportunities = (
        transformed_df["is_won"].sum()
    )

    lost_opportunities = (
        transformed_df["is_lost"].sum()
    )

    total_closed_value = (
        transformed_df.loc[
            transformed_df["is_closed"],
            "close_value",
        ].sum()
    )

    won_value = (
        transformed_df.loc[
            transformed_df["is_won"],
            "close_value",
        ].sum()
    )

    lost_value = (
        transformed_df.loc[
            transformed_df["is_lost"],
            "close_value",
        ].sum()
    )

    closed_outcomes = (
        won_opportunities
        + lost_opportunities
    )

    win_rate = (
        won_opportunities / closed_outcomes
        if closed_outcomes > 0
        else 0
    )

    return pd.DataFrame(
        [
            {
                "TotalOpportunities": total_opportunities,
                "OpenOpportunities": open_opportunities,
                "ClosedOpportunities": closed_opportunities,
                "WonOpportunities": won_opportunities,
                "LostOpportunities": lost_opportunities,
                "TotalClosedValue": total_closed_value,
                "WonValue": won_value,
                "LostValue": lost_value,
                "WinRatePct": win_rate * 100,
            }
        ]
    )

def build_stage_performance(transformed_df):
    """
    Build stage-level performance metrics
    for the Maven CRM pipeline.
    """

    stage_order = [
        "Prospecting",
        "Engaging",
        "Won",
        "Lost",
    ]

    stage_df = (
        transformed_df
        .groupby(
            [
                "deal_stage",
                "pipeline_status",
            ],
            as_index=False,
        )
        .agg(
            OpportunityCount=(
                "opportunity_id",
                "count",
            ),
            CloseValue=(
                "close_value",
                "sum",
            ),
            WonCount=(
                "is_won",
                "sum",
            ),
            LostCount=(
                "is_lost",
                "sum",
            ),
        )
    )

    total_opportunities = len(transformed_df)

    stage_df["OpportunitySharePct"] = (
        stage_df["OpportunityCount"]
        / total_opportunities
        * 100
    )

    stage_df["StageOrder"] = (
        stage_df["deal_stage"]
        .map(
            {
                "Prospecting": 1,
                "Engaging": 2,
                "Won": 3,
                "Lost": 4,
            }
        )
    )

    stage_df = (
        stage_df
        .sort_values("StageOrder")
        .drop(columns="StageOrder")
        .reset_index(drop=True)
    )

    return stage_df

def build_regional_performance(transformed_df):
    """
    Build regional performance metrics
    for the Maven CRM pipeline.
    """

    regional_df = (
        transformed_df
        .groupby(
            "regional_office",
            as_index=False,
        )
        .agg(
            OpportunityCount=(
                "opportunity_id",
                "count",
            ),
            CloseValue=(
                "close_value",
                "sum",
            ),
            WonCount=(
                "is_won",
                "sum",
            ),
            LostCount=(
                "is_lost",
                "sum",
            ),
        )
    )

    total_opportunities = len(transformed_df)

    regional_df["OpportunitySharePct"] = (
        regional_df["OpportunityCount"]
        / total_opportunities
        * 100
    )

    closed_outcomes = (
        regional_df["WonCount"]
        + regional_df["LostCount"]
    )

    regional_df["WinRatePct"] = (
        regional_df["WonCount"]
        / closed_outcomes
        * 100
    ).fillna(0)

    regional_df = (
        regional_df
        .sort_values(
            "WinRatePct",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return regional_df

def build_sales_agent_performance(transformed_df):
    """
    Build sales-agent performance metrics
    for the Maven CRM pipeline.
    """

    agent_df = (
        transformed_df
        .groupby(
            [
                "sales_agent",
                "manager",
                "regional_office",
            ],
            as_index=False,
        )
        .agg(
            OpportunityCount=(
                "opportunity_id",
                "count",
            ),
            CloseValue=(
                "close_value",
                "sum",
            ),
            WonCount=(
                "is_won",
                "sum",
            ),
            LostCount=(
                "is_lost",
                "sum",
            ),
        )
    )

    total_opportunities = len(transformed_df)

    agent_df["OpportunitySharePct"] = (
        agent_df["OpportunityCount"]
        / total_opportunities
        * 100
    )

    closed_outcomes = (
        agent_df["WonCount"]
        + agent_df["LostCount"]
    )

    agent_df["WinRatePct"] = (
        agent_df["WonCount"]
        / closed_outcomes
        * 100
    ).fillna(0)

    agent_df = (
        agent_df
        .sort_values(
            "WinRatePct",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return agent_df

def build_product_performance(transformed_df):
    """
    Build product-level performance metrics
    for the Maven CRM pipeline.
    """

    product_df = (
        transformed_df
        .groupby(
            "product_standardized",
            as_index=False,
        )
        .agg(
            OpportunityCount=(
                "opportunity_id",
                "count",
            ),
            CloseValue=(
                "close_value",
                "sum",
            ),
            WonCount=(
                "is_won",
                "sum",
            ),
            LostCount=(
                "is_lost",
                "sum",
            ),
        )
    )

    total_opportunities = len(transformed_df)

    product_df["OpportunitySharePct"] = (
        product_df["OpportunityCount"]
        / total_opportunities
        * 100
    )

    closed_outcomes = (
        product_df["WonCount"]
        + product_df["LostCount"]
    )

    product_df["WinRatePct"] = (
        product_df["WonCount"]
        / closed_outcomes
        * 100
    ).fillna(0)

    product_df = (
        product_df
        .sort_values(
            "CloseValue",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return product_df

def build_account_performance(
    transformed_df,
    accounts_df,
):
    """
    Build account-level performance metrics
    for the Maven CRM pipeline.
    """

    account_performance = (
        transformed_df[
            transformed_df["account"].notna()
        ]
        .groupby(
            "account",
            as_index=False,
        )
        .agg(
            OpportunityCount=(
                "opportunity_id",
                "count",
            ),
            CloseValue=(
                "close_value",
                "sum",
            ),
            WonCount=(
                "is_won",
                "sum",
            ),
            LostCount=(
                "is_lost",
                "sum",
            ),
        )
    )

    account_attributes = accounts_df[
        [
            "account",
            "sector",
            "year_established",
            "revenue",
            "employees",
            "office_location",
            "subsidiary_of",
        ]
    ].copy()

    account_df = account_attributes.merge(
        account_performance,
        on="account",
        how="left",
    )

    performance_columns = [
        "OpportunityCount",
        "CloseValue",
        "WonCount",
        "LostCount",
    ]

    account_df[performance_columns] = (
        account_df[performance_columns]
        .fillna(0)
    )

    total_opportunities = len(transformed_df)

    account_df["OpportunitySharePct"] = (
        account_df["OpportunityCount"]
        / total_opportunities
        * 100
    )

    closed_outcomes = (
        account_df["WonCount"]
        + account_df["LostCount"]
    )

    account_df["WinRatePct"] = (
        account_df["WonCount"]
        / closed_outcomes
        * 100
    ).fillna(0)

    account_df = (
        account_df
        .sort_values(
            "CloseValue",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return account_df
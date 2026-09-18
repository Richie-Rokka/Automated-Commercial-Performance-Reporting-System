def calculate_commercial_metrics(
    commercial_data_df,
    historical_cost_df,
    current_cost_df
):
    """
    Calculate reporting cost, gross profit,
    and gross margin at the sales-line grain.
    """

    reporting_df = commercial_data_df.merge(
        historical_cost_df[
            [
                "SalesOrderDetailID",
                "UnitCost"
            ]
        ],
        on="SalesOrderDetailID",
        how="left"
    )

    reporting_df = reporting_df.merge(
        current_cost_df,
        on="ProductID",
        how="left"
    )

    reporting_df["ReportingUnitCost"] = (
        reporting_df["UnitCost"]
        .fillna(
            reporting_df["CurrentStandardCost"]
        )
    )

    reporting_df["Cost"] = (
        reporting_df["OrderQty"]
        * reporting_df["ReportingUnitCost"]
    )

    reporting_df["GrossProfit"] = (
        reporting_df["Revenue"]
        - reporting_df["Cost"]
    )

    reporting_df["GrossMarginPct"] = (
        reporting_df["GrossProfit"]
        / reporting_df["Revenue"]
    ) * 100

    return reporting_df
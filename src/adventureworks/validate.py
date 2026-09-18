import numpy as np


def validate_row_population(
    reporting_df,
    expected_row_count
):
    """
    Validate that the reporting dataset contains
    the expected number of sales transactions.
    """

    actual_row_count = len(reporting_df)

    if actual_row_count != expected_row_count:
        raise ValueError(
            f"Row population validation failed. "
            f"Expected {expected_row_count:,} rows, "
            f"but received {actual_row_count:,}."
        )

    print(
        f"Row population validation: PASS "
        f"({actual_row_count:,} rows)"
    )


def validate_cost_completeness(reporting_df):
    """
    Validate that every reporting row has a
    resolved reporting unit cost.
    """

    unresolved_costs = (
        reporting_df["ReportingUnitCost"]
        .isna()
        .sum()
    )

    if unresolved_costs > 0:
        raise ValueError(
            f"Cost completeness validation failed. "
            f"{unresolved_costs:,} rows have no "
            f"ReportingUnitCost."
        )

    print("Cost completeness validation: PASS")


def validate_financial_reconciliation(reporting_df):
    """
    Validate the core gross-profit calculation.

    Gross Profit must equal:
        Revenue - Cost
    """

    total_revenue = reporting_df["Revenue"].sum()

    total_cost = reporting_df["Cost"].sum()

    total_gross_profit = (
        reporting_df["GrossProfit"].sum()
    )

    expected_gross_profit = (
        total_revenue - total_cost
    )

    difference = abs(
        total_gross_profit
        - expected_gross_profit
    )

    if difference >= 0.01:
        raise ValueError(
            "Financial reconciliation validation failed. "
            f"Difference: {difference:.10f}"
        )

    print(
        "Financial reconciliation validation: PASS "
        f"(difference: {difference:.10f})"
    )


def validate_financial_values(reporting_df):
    """
    Validate that core financial fields contain
    finite numeric values.
    """

    financial_columns = [
        "Revenue",
        "Cost",
        "GrossProfit",
        "GrossMarginPct",
    ]

    invalid_values = {}

    for column in financial_columns:

        values = reporting_df[column]

        missing_count = values.isna().sum()

        non_finite_count = (
            ~np.isfinite(values)
        ).sum()

        if missing_count > 0 or non_finite_count > 0:
            invalid_values[column] = {
                "missing": int(missing_count),
                "non_finite": int(non_finite_count),
            }

    if invalid_values:
        raise ValueError(
            "Financial value validation failed: "
            f"{invalid_values}"
        )

    print("Financial value validation: PASS")


def validate_reporting_data(
    reporting_df,
    expected_row_count
):
    """
    Run the essential validation controls for
    the AdventureWorks commercial reporting dataset.
    """

    validate_row_population(
        reporting_df,
        expected_row_count
    )

    validate_cost_completeness(
        reporting_df
    )

    validate_financial_reconciliation(
        reporting_df
    )

    validate_financial_values(
        reporting_df
    )

    print()
    print("Reporting data validation: PASS")
from pathlib import Path

from src.adventureworks.connection import create_database_engine
from src.adventureworks.datasets import build_reporting_datasets
from src.adventureworks.extract import (
    extract_commercial_data,
    extract_current_product_costs,
    extract_historical_costs,
)
from src.adventureworks.transform import calculate_commercial_metrics
from src.reporting.charts import add_reporting_charts
from src.reporting.formatting import format_report_workbook
from src.reporting.workbook import (
    build_report_workbook,
    save_workbook,
)


OUTPUT_PATH = Path(
    "reports/adventureworks_executive_report.xlsx"
)


def main():
    """
    Build, format, chart and structurally validate
    the reporting workbook.
    """

    # ---------------------------------------------------------
    # 1. Database connection
    # ---------------------------------------------------------

    engine = create_database_engine()

    # ---------------------------------------------------------
    # 2. Extraction
    # ---------------------------------------------------------

    commercial_data_df = extract_commercial_data(
        engine
    )

    historical_cost_df = extract_historical_costs(
        engine
    )

    current_cost_df = extract_current_product_costs(
        engine
    )

    # ---------------------------------------------------------
    # 3. Transformation
    # ---------------------------------------------------------

    reporting_df = calculate_commercial_metrics(
        commercial_data_df,
        historical_cost_df,
        current_cost_df,
    )

    # ---------------------------------------------------------
    # 4. Reporting datasets
    # ---------------------------------------------------------

    datasets = build_reporting_datasets(
        reporting_df
    )

    # ---------------------------------------------------------
    # 5. Workbook
    # ---------------------------------------------------------

    workbook = build_report_workbook(
        datasets
    )

    # ---------------------------------------------------------
    # 6. Formatting
    # ---------------------------------------------------------

    workbook = format_report_workbook(
        workbook
    )

    # ---------------------------------------------------------
    # 7. Charts
    # ---------------------------------------------------------

    workbook = add_reporting_charts(
        workbook
    )

    # ---------------------------------------------------------
    # 8. Structural validation
    # ---------------------------------------------------------

    expected_sheets = [
        "Executive Summary",
        "Monthly Performance",
        "Category Performance",
        "Product Performance",
        "Customer Performance",
        "Seller Performance",
    ]

    actual_sheets = workbook.sheetnames

    assert actual_sheets == expected_sheets, (
        "Worksheet structure validation failed.\n"
        f"Expected: {expected_sheets}\n"
        f"Actual: {actual_sheets}"
    )

    # ---------------------------------------------------------
    # Executive Summary
    # ---------------------------------------------------------

    executive = workbook[
        "Executive Summary"
    ]

    assert executive["A5"].value > 0
    assert executive["C5"].value > 0
    assert executive["E5"].value > 0

    executive_chart_count = len(
        executive._charts
    )

    assert executive_chart_count == 2, (
        "Expected 2 Executive Summary charts, "
        f"found {executive_chart_count}."
    )

    print(
        "Executive Summary charts: "
        f"{executive_chart_count}"
    )

    # ---------------------------------------------------------
    # Category Performance
    # ---------------------------------------------------------

    category = workbook[
        "Category Performance"
    ]

    category_data_rows = (
        category.max_row - 5
    )

    assert category["A6"].value is not None
    assert category["B6"].value > 0

    category_chart_count = len(
        category._charts
    )

    assert category_chart_count == 2, (
        "Expected 2 Category Performance charts, "
        f"found {category_chart_count}."
    )

    print(
        "Category Performance charts: "
        f"{category_chart_count}"
    )

    # ---------------------------------------------------------
    # Product Performance
    # ---------------------------------------------------------

    product = workbook[
        "Product Performance"
    ]

    top_product_rows = 15

    assert product["A6"].value is not None
    assert product["B6"].value is not None

    # Rows 6–20 contain the 15 top-revenue products.
    actual_top_product_rows = (
        20 - 6 + 1
    )

    assert actual_top_product_rows == top_product_rows

    assert (
        product["E6"].value
        >= product["E7"].value
    )

    product_chart_count = len(
        product._charts
    )

    assert product_chart_count == 2, (
        "Expected 2 Product Performance charts, "
        f"found {product_chart_count}."
    )

    print(
        "Product Performance top products: "
        f"{actual_top_product_rows}"
    )

    print(
        "Product Performance charts: "
        f"{product_chart_count}"
    )

    # ---------------------------------------------------------
    # Customer Performance
    # ---------------------------------------------------------

    customer = workbook[
        "Customer Performance"
    ]

    assert customer.max_row > 1

    # ---------------------------------------------------------
    # Seller Performance
    # ---------------------------------------------------------

    seller = workbook[
        "Seller Performance"
    ]

    assert seller.max_row > 1

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    output_path = save_workbook(
        workbook,
        OUTPUT_PATH,
    )

    print()
    print("Workbook created successfully.")
    print(f"Path: {output_path}")

    print()
    print("Worksheets:")

    for worksheet in workbook.worksheets:
        print(f"- {worksheet.title}")


if __name__ == "__main__":
    main()
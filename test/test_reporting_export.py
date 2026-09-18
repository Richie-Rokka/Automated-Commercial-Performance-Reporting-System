from pathlib import Path

from src.adventureworks.connection import create_database_engine
from src.adventureworks.extract import extract_commercial_data
from src.adventureworks.extract import extract_historical_costs
from src.adventureworks.extract import extract_current_product_costs
from src.adventureworks.transform import calculate_commercial_metrics
from src.adventureworks.validate import validate_reporting_data
from src.adventureworks.datasets import build_reporting_datasets
from src.reporting.export import (
    export_reporting_datasets_with_summary,
)


OUTPUT_DIRECTORY = Path("data/reporting")


def main():

    print("Creating database engine...")

    engine = create_database_engine()

    print("Extracting commercial data...")

    commercial_data = extract_commercial_data(
        engine
    )

    print("Extracting historical costs...")

    historical_costs = extract_historical_costs(
        engine
    )

    print("Extracting current product costs...")

    current_costs = extract_current_product_costs(
        engine
    )

    print("Calculating commercial metrics...")

    reporting_data = calculate_commercial_metrics(
        commercial_data,
        historical_costs,
        current_costs,
    )

    print("Validating reporting data...")

    validate_reporting_data(
        reporting_data,
        expected_row_count=len(commercial_data),
    )

    print("Building reporting datasets...")

    datasets = build_reporting_datasets(
        reporting_data
    )

    export_reporting_datasets_with_summary(
        datasets,
        OUTPUT_DIRECTORY,
    )

    print()
    print("Reporting export completed successfully.")


if __name__ == "__main__":
    main()
from pathlib import Path

import pandas as pd


DEFAULT_OUTPUT_DIRECTORY = Path("data/reporting")


def export_reporting_datasets(
    datasets,
    output_directory=DEFAULT_OUTPUT_DIRECTORY,
):
    """
    Export reporting datasets to CSV files for Power BI.

    Parameters
    ----------
    datasets : dict
        Dictionary returned by build_reporting_datasets().

    output_directory : Path or str
        Directory where reporting CSV files will be written.

    Returns
    -------
    dict
        Dictionary containing the paths of the exported files.
    """

    output_directory = Path(output_directory)

    # Create the directory if it does not already exist.
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    exported_files = {}

    # ---------------------------------------------------------
    # Executive KPIs
    # ---------------------------------------------------------

    executive_path = (
        output_directory / "executive_kpis.csv"
    )

    datasets["executive_kpis"].to_csv(
        executive_path,
        index=False,
    )

    exported_files["executive_kpis"] = executive_path

    # ---------------------------------------------------------
    # Monthly Performance
    # ---------------------------------------------------------

    monthly_path = (
        output_directory / "monthly_performance.csv"
    )

    datasets["monthly_performance"].to_csv(
        monthly_path,
        index=False,
    )

    exported_files["monthly_performance"] = monthly_path

    # ---------------------------------------------------------
    # Category Performance
    # ---------------------------------------------------------

    category_path = (
        output_directory / "category_performance.csv"
    )

    datasets["category_performance"].to_csv(
        category_path,
        index=False,
    )

    exported_files["category_performance"] = category_path

    # ---------------------------------------------------------
    # Product Performance
    # ---------------------------------------------------------

    product_path = (
        output_directory / "product_performance.csv"
    )

    datasets["product_performance"].to_csv(
        product_path,
        index=False,
    )

    exported_files["product_performance"] = product_path

    # ---------------------------------------------------------
    # Customer Performance
    # ---------------------------------------------------------

    customer_path = (
        output_directory / "customer_performance.csv"
    )

    datasets["customer_performance"].to_csv(
        customer_path,
        index=False,
    )

    exported_files["customer_performance"] = customer_path

    # ---------------------------------------------------------
    # Seller Performance
    # ---------------------------------------------------------

    seller_path = (
        output_directory / "seller_performance.csv"
    )

    datasets["seller_performance"].to_csv(
        seller_path,
        index=False,
    )

    exported_files["seller_performance"] = seller_path

    # ---------------------------------------------------------
    # Key Observations
    # ---------------------------------------------------------

    observations_path = (
        output_directory / "key_observations.csv"
    )

    observations_df = pd.DataFrame(
        {
            "Observation": datasets["key_observations"]
        }
    )

    observations_df.to_csv(
        observations_path,
        index=False,
    )

    exported_files["key_observations"] = (
        observations_path
    )

    return exported_files


def export_reporting_datasets_with_summary(
    datasets,
    output_directory=DEFAULT_OUTPUT_DIRECTORY,
):
    """
    Export reporting datasets and print a concise
    execution summary.

    This is useful during development and testing.
    """

    exported_files = export_reporting_datasets(
        datasets,
        output_directory,
    )

    print()
    print("REPORTING DATA EXPORT")
    print("=" * 60)

    for dataset_name, file_path in exported_files.items():

        if dataset_name == "key_observations":
            row_count = len(
                datasets[dataset_name]
            )

        else:
            row_count = len(
                datasets[dataset_name]
            )

        print(
            f"{dataset_name:<25}"
            f"{row_count:>10,} rows    "
            f"{file_path}"
        )

    print("=" * 60)
    print(
        f"Exported {len(exported_files)} reporting datasets."
    )

    return exported_files
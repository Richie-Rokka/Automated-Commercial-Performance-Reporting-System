from pathlib import Path


DEFAULT_OUTPUT_DIRECTORY = Path("data/reporting/maven_crm")


def export_maven_reporting_datasets(
    datasets,
    output_directory=DEFAULT_OUTPUT_DIRECTORY,
):
    """
    Export Maven CRM reporting datasets
    to CSV files for Power BI.
    """

    output_directory = Path(output_directory)
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    exported_files = {}

    export_map = {
        "executive_pipeline_kpis": "executive_pipeline_kpis.csv",
        "stage_performance": "stage_performance.csv",
        "regional_performance": "regional_performance.csv",
        "sales_agent_performance": "sales_agent_performance.csv",
        "product_performance": "product_performance.csv",
        "account_performance": "account_performance.csv",
    }

    for dataset_name, filename in export_map.items():
        file_path = output_directory / filename

        datasets[dataset_name].to_csv(
            file_path,
            index=False,
        )

        exported_files[dataset_name] = file_path

    return exported_files


def export_maven_reporting_datasets_with_summary(
    datasets,
    output_directory=DEFAULT_OUTPUT_DIRECTORY,
):
    """
    Export Maven CRM reporting datasets
    and print an execution summary.
    """

    exported_files = export_maven_reporting_datasets(
        datasets,
        output_directory,
    )

    print()
    print("MAVEN CRM REPORTING EXPORT")
    print("=" * 70)

    for dataset_name, file_path in exported_files.items():
        row_count = len(
            datasets[dataset_name]
        )

        print(
            f"{dataset_name:<30}"
            f"{row_count:>10,} rows    "
            f"{file_path}"
        )

    print("=" * 70)

    print(
        f"Exported {len(exported_files)} "
        "reporting datasets."
    )

    return exported_files
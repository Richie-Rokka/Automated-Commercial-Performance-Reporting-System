from pathlib import Path

import pandas as pd


DEFAULT_SOURCE_DIRECTORY = Path(
    "data/raw/maven_crm"
)


def extract_sales_pipeline(
    source_directory=DEFAULT_SOURCE_DIRECTORY,
):
    """
    Extract the Maven CRM sales pipeline.

    Grain:
        One row per sales opportunity.
    """
    file_path = (
        Path(source_directory)
        / "sales_pipeline.csv"
    )

    sales_pipeline_df = pd.read_csv(file_path)

    return sales_pipeline_df


def extract_accounts(
    source_directory=DEFAULT_SOURCE_DIRECTORY,
):
    """
    Extract the Maven CRM account master.
    """
    file_path = (
        Path(source_directory)
        / "accounts.csv"
    )

    accounts_df = pd.read_csv(file_path)

    return accounts_df


def extract_products(
    source_directory=DEFAULT_SOURCE_DIRECTORY,
):
    """
    Extract the Maven CRM product master.
    """
    file_path = (
        Path(source_directory)
        / "products.csv"
    )

    products_df = pd.read_csv(file_path)

    return products_df


def extract_sales_teams(
    source_directory=DEFAULT_SOURCE_DIRECTORY,
):
    """
    Extract the Maven CRM sales-team master.
    """
    file_path = (
        Path(source_directory)
        / "sales_teams.csv"
    )

    sales_teams_df = pd.read_csv(file_path)

    return sales_teams_df
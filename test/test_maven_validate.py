from src.maven_crm.extract import (
    extract_accounts,
    extract_products,
    extract_sales_pipeline,
    extract_sales_teams,
)

from src.maven_crm.validate import validate_maven_data


def main():
    print("Extracting Maven CRM data...")

    sales_pipeline_df = extract_sales_pipeline()
    accounts_df = extract_accounts()
    products_df = extract_products()
    sales_teams_df = extract_sales_teams()

    print("Extraction completed.")
    print()

    validate_maven_data(
        sales_pipeline_df=sales_pipeline_df,
        accounts_df=accounts_df,
        products_df=products_df,
        sales_teams_df=sales_teams_df,
    )


if __name__ == "__main__":
    main()
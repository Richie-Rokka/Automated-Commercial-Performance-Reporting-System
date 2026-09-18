from src.maven_crm.extract import (
    extract_accounts,
    extract_products,
    extract_sales_pipeline,
    extract_sales_teams,
)


def main():
    sales_pipeline_df = extract_sales_pipeline()
    accounts_df = extract_accounts()
    products_df = extract_products()
    sales_teams_df = extract_sales_teams()

    print("MAVEN CRM EXTRACTION")
    print("=" * 60)

    print(
        f"sales_pipeline : "
        f"{len(sales_pipeline_df):>6,} rows"
    )

    print(
        f"accounts       : "
        f"{len(accounts_df):>6,} rows"
    )

    print(
        f"products       : "
        f"{len(products_df):>6,} rows"
    )

    print(
        f"sales_teams    : "
        f"{len(sales_teams_df):>6,} rows"
    )


if __name__ == "__main__":
    main()
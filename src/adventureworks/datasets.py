import pandas as pd


def build_executive_kpis(reporting_df):
    """
    Build the one-row executive KPI dataset.

    The reporting DataFrame is already calculated at the
    sales-line grain. This function aggregates those results
    for management reporting.
    """

    total_revenue = reporting_df["Revenue"].sum()
    total_cost = reporting_df["Cost"].sum()
    total_gross_profit = reporting_df["GrossProfit"].sum()

    gross_margin_pct = (
        total_gross_profit / total_revenue
    ) * 100

    return pd.DataFrame(
        [
            {
                "Revenue": total_revenue,
                "Cost": total_cost,
                "GrossProfit": total_gross_profit,
                "GrossMarginPct": gross_margin_pct,
                "UnitsSold": reporting_df["OrderQty"].sum(),
                "Customers": reporting_df["CustomerID"].nunique(),
                "Products": reporting_df["ProductID"].nunique(),
            }
        ]
    )


def build_monthly_performance(reporting_df):
    """
    Build monthly commercial performance.

    Grain:
        One row per reporting month.
    """

    monthly_df = reporting_df.copy()

    monthly_df["OrderMonth"] = (
        pd.to_datetime(
            monthly_df["OrderDate"]
        )
        .dt.to_period("M")
        .astype(str)
    )

    monthly_df = (
        monthly_df
        .groupby("OrderMonth", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            GrossProfit=("GrossProfit", "sum"),
            SalesLines=("SalesOrderDetailID", "nunique"),
            Units=("OrderQty", "sum"),
        )
    )

    monthly_df["GrossMarginPct"] = (
        monthly_df["GrossProfit"]
        / monthly_df["Revenue"]
    ) * 100

    monthly_df["RevenueChangePct"] = (
        monthly_df["Revenue"]
        .pct_change()
        * 100
    )

    monthly_df["GrossProfitChangePct"] = (
        monthly_df["GrossProfit"]
        .pct_change()
        * 100
    )

    monthly_df["MarginChangePts"] = (
        monthly_df["GrossMarginPct"]
        .diff()
    )

    # The final period is June 2014 and is treated as a
    # final/partial reporting period rather than a normal
    # completed month.
    monthly_df["IsFinalPeriod"] = (
        monthly_df["OrderMonth"]
        == monthly_df["OrderMonth"].max()
    )

    return monthly_df


def build_category_performance(reporting_df):
    """
    Build category-level commercial performance.
    """

    category_df = (
        reporting_df
        .groupby(
            "ProductCategory",
            dropna=False,
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            GrossProfit=("GrossProfit", "sum"),
            Units=("OrderQty", "sum"),
            SalesLines=("SalesOrderDetailID", "nunique"),
            Products=("ProductID", "nunique"),
        )
        .reset_index()
    )

    category_df["GrossMarginPct"] = (
        category_df["GrossProfit"]
        / category_df["Revenue"]
    ) * 100

    total_revenue = category_df["Revenue"].sum()

    category_df["RevenueSharePct"] = (
        category_df["Revenue"]
        / total_revenue
    ) * 100

    return category_df.sort_values(
        "Revenue",
        ascending=False,
    ).reset_index(drop=True)


def build_product_performance(reporting_df):
    """
    Build the complete product-level commercial dataset.

    Grain:
        One row per product.
    """

    product_df = (
        reporting_df
        .groupby(
            [
                "ProductID",
                "ProductName",
                "ProductCategory",
                "ProductSubcategory",
            ],
            dropna=False,
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            GrossProfit=("GrossProfit", "sum"),
            Units=("OrderQty", "sum"),
            SalesLines=("SalesOrderDetailID", "nunique"),
        )
        .reset_index()
    )

    product_df["GrossMarginPct"] = (
        product_df["GrossProfit"]
        / product_df["Revenue"]
    ) * 100

    return product_df.sort_values(
        "Revenue",
        ascending=False,
    ).reset_index(drop=True)


def build_top_products(
    product_performance_df,
    top_n=15,
):
    """
    Build the management view of the highest-revenue products.

    Parameters
    ----------
    product_performance_df : pandas.DataFrame
        Complete product performance dataset.

    top_n : int
        Number of products to return.
    """

    return (
        product_performance_df
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .head(top_n)
        .reset_index(drop=True)
    )


def build_product_margin_risk(
    product_performance_df,
    candidate_n=50,
    risk_n=10,
):
    """
    Identify low-margin products within the highest-revenue
    product population.

    The purpose is to focus management attention on margin
    risk that is commercially material rather than selecting
    tiny products with negligible revenue.

    Process:
        1. Select the top 50 products by revenue.
        2. Rank those products by gross margin.
        3. Return the 10 lowest-margin products.
    """

    candidate_products = (
        product_performance_df
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .head(candidate_n)
    )

    risk_df = (
        candidate_products
        .sort_values(
            [
                "GrossMarginPct",
                "Revenue",
            ],
            ascending=[
                True,
                False,
            ],
        )
        .head(risk_n)
        .reset_index(drop=True)
    )

    return risk_df


def build_customer_performance(reporting_df):
    """
    Build customer-level commercial performance.
    """

    customer_df = reporting_df.copy()

    customer_df["CustomerName"] = (
        customer_df["FirstName"]
        .fillna("")
        .str.strip()
        .str.cat(
            customer_df["LastName"]
            .fillna("")
            .str.strip(),
            sep=" ",
        )
        .str.strip()
    )

    customer_df = (
        customer_df
        .groupby(
            [
                "CustomerID",
                "AccountNumber",
                "CustomerName",
            ],
            dropna=False,
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            GrossProfit=("GrossProfit", "sum"),
            Units=("OrderQty", "sum"),
            SalesLines=("SalesOrderDetailID", "nunique"),
            Products=("ProductID", "nunique"),
        )
        .reset_index()
    )

    customer_df["GrossMarginPct"] = (
        customer_df["GrossProfit"]
        / customer_df["Revenue"]
    ) * 100

    return customer_df.sort_values(
        "Revenue",
        ascending=False,
    ).reset_index(drop=True)


def build_seller_performance(reporting_df):
    """
    Build salesperson-level commercial performance.

    Transactions without an assigned salesperson remain in
    the underlying reporting data but are excluded from this
    salesperson-specific view.
    """

    seller_df = reporting_df[
        reporting_df["SalesPersonID"].notna()
    ].copy()

    seller_df = (
        seller_df
        .groupby(
            [
                "SalesPersonID",
                "SalesPersonFirstName",
                "SalesPersonLastName",
            ],
            dropna=False,
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Cost=("Cost", "sum"),
            GrossProfit=("GrossProfit", "sum"),
            Units=("OrderQty", "sum"),
            SalesLines=("SalesOrderDetailID", "nunique"),
            Products=("ProductID", "nunique"),
        )
        .reset_index()
    )

    seller_df["SalesPersonName"] = (
        seller_df["SalesPersonFirstName"]
        .fillna("")
        .str.strip()
        .str.cat(
            seller_df["SalesPersonLastName"]
            .fillna("")
            .str.strip(),
            sep=" ",
        )
        .str.strip()
    )

    seller_df = seller_df[
        [
            "SalesPersonID",
            "SalesPersonName",
            "Revenue",
            "Cost",
            "GrossProfit",
            "Units",
            "SalesLines",
            "Products",
        ]
    ]

    seller_df["GrossMarginPct"] = (
        seller_df["GrossProfit"]
        / seller_df["Revenue"]
    ) * 100

    return seller_df.sort_values(
        "Revenue",
        ascending=False,
    ).reset_index(drop=True)


def build_key_observations(
    executive_kpis_df,
    category_df,
    product_df,
    customer_df,
    seller_df,
    monthly_df,
):
    """
    Build deterministic management observations.

    These observations are generated from the same reporting
    datasets used by the report. No external intelligence or
    AI-generated commentary is involved.
    """

    observations = []

    executive = executive_kpis_df.iloc[0]

    # ---------------------------------------------------------
    # Category observation
    # ---------------------------------------------------------

    top_category = category_df.iloc[0]

    observations.append(
        f"{top_category['ProductCategory']} generated "
        f"{top_category['RevenueSharePct']:.1f}% of total revenue."
    )

    # ---------------------------------------------------------
    # Lowest category margin
    # ---------------------------------------------------------

    lowest_margin_category = category_df.loc[
        category_df["GrossMarginPct"].idxmin()
    ]

    observations.append(
        f"{lowest_margin_category['ProductCategory']} reported "
        f"the lowest category margin at "
        f"{lowest_margin_category['GrossMarginPct']:.2f}%, "
        f"below company average of "
        f"{executive['GrossMarginPct']:.2f}%."
    )

    # ---------------------------------------------------------
    # Customer margin risk
    # ---------------------------------------------------------

    top_customers = customer_df.head(15)

    negative_customer_count = (
        top_customers["GrossProfit"] < 0
    ).sum()

    if negative_customer_count > 0:
        observations.append(
            f"{negative_customer_count} of the top 15 customers "
            "by revenue generated negative gross profit."
        )

    # ---------------------------------------------------------
    # Seller margin risk
    # ---------------------------------------------------------

    negative_seller_count = (
        seller_df["GrossProfit"] < 0
    ).sum()

    if negative_seller_count > 0:
        lowest_margin_seller = seller_df.loc[
            seller_df["GrossMarginPct"].idxmin()
        ]

        observations.append(
            f"{negative_seller_count} of "
            f"{len(seller_df)} sellers generated negative "
            f"gross profit; "
            f"{lowest_margin_seller['SalesPersonName']} "
            f"had the lowest margin at "
            f"{lowest_margin_seller['GrossMarginPct']:.2f}%."
        )

    # ---------------------------------------------------------
    # Product margin risk
    # ---------------------------------------------------------

    top_products = product_df.head(15)

    low_margin_products = top_products[
        top_products["GrossMarginPct"] < 5
    ]

    if not low_margin_products.empty:
        lowest_product = low_margin_products.loc[
            low_margin_products["GrossMarginPct"].idxmin()
        ]

        observations.append(
            f"{lowest_product['ProductName']} is among the "
            "top-revenue products but generated only "
            f"{lowest_product['GrossMarginPct']:.2f}% "
            "gross margin."
        )

    return observations[:5]


def build_reporting_datasets(reporting_df):
    """
    Build all datasets required by the reporting layer.
    """

    executive_kpis_df = build_executive_kpis(
        reporting_df
    )

    monthly_df = build_monthly_performance(
        reporting_df
    )

    category_df = build_category_performance(
        reporting_df
    )

    product_df = build_product_performance(
        reporting_df
    )

    top_products_df = build_top_products(
        product_df,
        top_n=15,
    )

    product_margin_risk_df = build_product_margin_risk(
        product_df,
        candidate_n=50,
        risk_n=10,
    )

    customer_df = build_customer_performance(
        reporting_df
    )

    seller_df = build_seller_performance(
        reporting_df
    )

    observations = build_key_observations(
        executive_kpis_df,
        category_df,
        product_df,
        customer_df,
        seller_df,
        monthly_df,
    )

    return {
        "executive_kpis": executive_kpis_df,
        "monthly_performance": monthly_df,
        "category_performance": category_df,
        "product_performance": product_df,
        "top_products": top_products_df,
        "product_margin_risk": product_margin_risk_df,
        "customer_performance": customer_df,
        "seller_performance": seller_df,
        "key_observations": observations,
    }
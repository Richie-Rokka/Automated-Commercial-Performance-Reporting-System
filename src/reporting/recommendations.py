from math import ceil
from pathlib import Path

import pandas as pd


DEFAULT_OUTPUT_DIRECTORY = Path("data/reporting")


def _format_currency_millions(value):
    """
    Format a monetary value in millions for management reporting.
    """
    return f"${value / 1_000_000:.1f}M"


def _format_percentage(value):
    """
    Format a percentage value to two decimal places.
    """
    return f"{value:.2f}%"


def _build_recommendation(
    recommendation_id,
    priority,
    area,
    finding,
    recommendation,
    metric,
):
    """
    Create one standardized management recommendation.
    """
    return {
        "RecommendationID": recommendation_id,
        "Priority": priority,
        "Area": area,
        "Finding": finding,
        "Recommendation": recommendation,
        "Metric": metric,
    }


def build_margin_recommendation(
    executive_kpis,
    category_df,
    product_df,
):
    """
    Evaluate category and product margin performance.

    A margin issue is flagged when:
        - a category is at least 2 percentage points below
          the overall company margin, or
        - a high-revenue product is at least 5 percentage
          points below the overall company margin.

    This uses relative performance thresholds rather than
    hard-coded product or category names.
    """

    if not isinstance(executive_kpis, dict):
        raise TypeError(
            "executive_kpis must be the AdventureWorks executive KPI dictionary."
        )

    if "gross_margin_pct" not in executive_kpis:
        raise KeyError(
            "AdventureWorks executive KPIs must contain 'gross_margin_pct'."
        )

    company_margin = float(
        executive_kpis["gross_margin_pct"]
    )

    category_df = category_df.copy()

    category_df["MarginGapPct"] = (
        category_df["GrossMarginPct"]
        - company_margin
    )

    weak_categories = (
        category_df[
            category_df["MarginGapPct"] <= -2
        ]
        .sort_values("MarginGapPct")
    )

    product_count = len(product_df)

    top_product_count = max(
        1,
        ceil(product_count * 0.15),
    )

    high_revenue_products = (
        product_df
        .nlargest(top_product_count, "Revenue")
        .copy()
    )

    weak_products = (
        high_revenue_products[
            high_revenue_products["GrossMarginPct"]
            <= company_margin - 5
        ]
        .sort_values("GrossMarginPct")
    )

    finding_parts = []

    if not weak_categories.empty:
        category = weak_categories.iloc[0]

        finding_parts.append(
            f"{category['ProductCategory']} margin is "
            f"{_format_percentage(category['GrossMarginPct'])}, "
            f"{abs(category['MarginGapPct']):.2f} percentage points "
            f"below the company margin."
        )

    if not weak_products.empty:
        product = weak_products.iloc[0]

        finding_parts.append(
            f"{product['ProductName']} generates "
            f"{_format_currency_millions(product['Revenue'])} "
            f"revenue at only "
            f"{_format_percentage(product['GrossMarginPct'])} margin."
        )

    if finding_parts:
        finding = " ".join(finding_parts)

        return _build_recommendation(
            recommendation_id=1,
            priority="High",
            area="Gross Margin",
            finding=finding,
            recommendation=(
                "Review pricing, discounting, product mix, "
                "and cost drivers for low-margin business."
            ),
            metric=_format_percentage(company_margin),
        )

    return _build_recommendation(
        recommendation_id=1,
        priority="Low",
        area="Gross Margin",
        finding=(
            "No material category or high-revenue product "
            "margin exception was detected."
        ),
        recommendation=(
            "Continue monitoring margin performance "
            "across categories and high-revenue products."
        ),
        metric=_format_percentage(company_margin),
    )


def build_customer_profitability_recommendation(
    customer_df,
    top_n=15,
):
    """
    Evaluate profitability among the highest-revenue customers.

    A customer profitability issue is flagged when one or more
    of the top-N customers by revenue has negative gross profit.
    """

    top_customers = (
        customer_df
        .nlargest(top_n, "Revenue")
        .copy()
    )

    loss_making_customers = top_customers[
        top_customers["GrossProfit"] < 0
    ]

    loss_count = len(loss_making_customers)

    if loss_count > 0:
        finding = (
            f"{loss_count} of the top {len(top_customers)} "
            "customers by revenue generated negative gross profit."
        )

        return _build_recommendation(
            recommendation_id=2,
            priority="High",
            area="Customer Profitability",
            finding=finding,
            recommendation=(
                "Conduct account-level profitability reviews "
                "and investigate pricing, discounting, product mix, "
                "and cost-to-serve."
            ),
            metric=f"{loss_count} / {len(top_customers)}",
        )

    return _build_recommendation(
        recommendation_id=2,
        priority="Low",
        area="Customer Profitability",
        finding=(
            f"No loss-making customers were identified "
            f"among the top {len(top_customers)} customers by revenue."
        ),
        recommendation=(
            "Continue monitoring customer-level profitability "
            "and revenue concentration."
        ),
        metric=f"0 / {len(top_customers)}",
    )


def build_seller_profitability_recommendation(
    seller_df,
):
    """
    Evaluate seller-level gross profit performance.

    A seller profitability issue is flagged when one or more
    active sellers has negative gross profit.
    """

    active_sellers = len(seller_df)

    loss_making_sellers = seller_df[
        seller_df["GrossProfit"] < 0
    ]

    loss_count = len(loss_making_sellers)

    if loss_count > 0:
        lowest_margin_seller = (
            loss_making_sellers
            .sort_values("GrossMarginPct")
            .iloc[0]
        )

        if "SalesPersonName" in lowest_margin_seller.index:
            seller_name = lowest_margin_seller["SalesPersonName"]
        elif {
            "SalesPersonFirstName",
            "SalesPersonLastName",
        }.issubset(lowest_margin_seller.index):
            seller_name = (
                f"{lowest_margin_seller['SalesPersonFirstName']} "
                f"{lowest_margin_seller['SalesPersonLastName']}"
            )
        else:
            seller_name = (
                f"SalesPersonID {lowest_margin_seller['SalesPersonID']}"
            )

        finding = (
            f"{loss_count} of {active_sellers} active sellers "
            f"generated negative gross profit. "
            f"{seller_name} "
            f"had the lowest margin at "
            f"{_format_percentage(lowest_margin_seller['GrossMarginPct'])}."
        )

        return _build_recommendation(
            recommendation_id=3,
            priority="High",
            area="Seller Profitability",
            finding=finding,
            recommendation=(
                "Review seller-level pricing, discounting, "
                "product mix, and account allocation to identify "
                "drivers of negative gross profit."
            ),
            metric=f"{loss_count} / {active_sellers}",
        )

    return _build_recommendation(
        recommendation_id=3,
        priority="Low",
        area="Seller Profitability",
        finding=(
            "No active sellers generated negative gross profit."
        ),
        recommendation=(
            "Continue monitoring seller profitability "
            "and commercial mix."
        ),
        metric=f"0 / {active_sellers}",
    )


def build_pipeline_visibility_recommendation(
    transformed_pipeline_df,
):
    """
    Evaluate completeness of key commercial fields
    for open CRM opportunities.

    Open opportunities should have:
        - close_date
        - close_value

    The recommendation does not invent a value for missing
    open pipeline. It flags the visibility limitation itself.
    """

    open_pipeline = transformed_pipeline_df[
        transformed_pipeline_df["is_open"]
    ].copy()

    open_count = len(open_pipeline)

    missing_close_value = (
        open_pipeline["close_value"].isna()
    )

    missing_close_date = (
        open_pipeline["close_date"].isna()
    )

    missing_either = (
        missing_close_value
        | missing_close_date
    )

    incomplete_count = int(
        missing_either.sum()
    )

    if incomplete_count > 0:
        finding = (
            f"{incomplete_count:,} of {open_count:,} "
            "open opportunities lack required close-value "
            "or close-date information."
        )

        return _build_recommendation(
            recommendation_id=4,
            priority="Medium/High",
            area="Pipeline Visibility",
            finding=finding,
            recommendation=(
                "Improve CRM pipeline discipline by requiring "
                "expected close value and close-date information "
                "for open opportunities."
            ),
            metric=f"{incomplete_count:,}",
        )

    return _build_recommendation(
        recommendation_id=4,
        priority="Low",
        area="Pipeline Visibility",
        finding=(
            "Open opportunities contain the required "
            "close-value and close-date information."
        ),
        recommendation=(
            "Maintain CRM completeness standards "
            "and monitor them during future refreshes."
        ),
        metric=f"{open_count:,}",
    )


def build_pipeline_prioritization_recommendation(
    regional_df,
    product_df,
):
    """
    Identify where management should focus pipeline attention.

    The recommendation considers:
        - region with the highest opportunity volume
        - region with the highest win rate
        - product with the highest closed value
    """

    highest_volume_region = (
        regional_df
        .sort_values(
            "OpportunityCount",
            ascending=False,
        )
        .iloc[0]
    )

    highest_win_rate_region = (
        regional_df
        .sort_values(
            "WinRatePct",
            ascending=False,
        )
        .iloc[0]
    )

    highest_value_product = (
        product_df
        .sort_values(
            "CloseValue",
            ascending=False,
        )
        .iloc[0]
    )

    finding = (
        f"{highest_volume_region['regional_office']} has the "
        f"largest opportunity volume at "
        f"{int(highest_volume_region['OpportunityCount']):,}. "
        f"{highest_win_rate_region['regional_office']} has the "
        f"highest win rate at "
        f"{_format_percentage(highest_win_rate_region['WinRatePct'])}. "
        f"{highest_value_product['product_standardized']} "
        f"has the highest closed value at "
        f"{_format_currency_millions(highest_value_product['CloseValue'])}."
    )

    recommendation = (
        f"Prioritize high-volume opportunities in "
        f"{highest_volume_region['regional_office']} while "
        f"examining the conversion practices of "
        f"{highest_win_rate_region['regional_office']}. "
        f"Focus product attention on "
        f"{highest_value_product['product_standardized']}."
    )

    return _build_recommendation(
        recommendation_id=5,
        priority="Medium",
        area="Pipeline Prioritization",
        finding=finding,
        recommendation=recommendation,
        metric=(
            f"{int(highest_volume_region['OpportunityCount']):,} "
            "opportunities"
        ),
    )


def build_management_recommendations(
    executive_kpis,
    category_df,
    adventureworks_product_df,
    customer_df,
    seller_df,
    transformed_pipeline_df,
    regional_df,
    maven_product_df,
):
    """
    Build the complete management recommendation dataset.

    The function evaluates current reporting outputs and returns
    one standardized recommendation for each management area.
    """

    recommendations = [
        build_margin_recommendation(
            executive_kpis,
            category_df,
            adventureworks_product_df,
        ),
        build_customer_profitability_recommendation(
            customer_df,
        ),
        build_seller_profitability_recommendation(
            seller_df,
        ),
        build_pipeline_visibility_recommendation(
            transformed_pipeline_df,
        ),
        build_pipeline_prioritization_recommendation(
            regional_df,
            maven_product_df,
        ),
    ]

    return pd.DataFrame(recommendations)


def export_management_recommendations(
    recommendations_df,
    output_directory=DEFAULT_OUTPUT_DIRECTORY,
):
    """
    Export management recommendations for Power BI.
    """

    output_directory = Path(
        output_directory
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_directory
        / "management_recommendations.csv"
    )

    recommendations_df.to_csv(
        output_path,
        index=False,
    )

    return output_path


def export_management_recommendations_with_summary(
    recommendations_df,
    output_directory=DEFAULT_OUTPUT_DIRECTORY,
):
    """
    Export recommendations and print an execution summary.
    """

    output_path = export_management_recommendations(
        recommendations_df,
        output_directory,
    )

    print()
    print("MANAGEMENT RECOMMENDATIONS")
    print("=" * 80)

    for _, row in recommendations_df.iterrows():
        print(
            f"{int(row['RecommendationID']):02d} "
            f"{row['Priority']:<12} "
            f"{row['Area']:<25} "
            f"{row['Metric']}"
        )

    print("=" * 80)
    print(
        f"Exported {len(recommendations_df)} "
        f"management recommendations."
    )

    print(
        f"Output: {output_path}"
    )

    return output_path
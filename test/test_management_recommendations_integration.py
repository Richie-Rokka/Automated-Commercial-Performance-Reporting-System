from pathlib import Path

import pandas as pd

from src.reporting.recommendations import build_management_recommendations
from src.generate_management_recommendations import (
    build_adventureworks_reporting_data,
    build_maven_reporting_data,
)


def test_real_reporting_datasets_produce_management_recommendations():
    """
    Integration test.

    Uses the project's real AdventureWorks database and Maven CRM source
    files rather than synthetic unit-test fixtures.
    """
    adventureworks = build_adventureworks_reporting_data()
    maven = build_maven_reporting_data()

    recommendations_df = build_management_recommendations(
        executive_kpis=adventureworks["executive"],
        category_df=adventureworks["category"],
        adventureworks_product_df=adventureworks["product"],
        customer_df=adventureworks["customer"],
        seller_df=adventureworks["seller"],
        transformed_pipeline_df=maven["transformed_pipeline"],
        regional_df=maven["regional"],
        maven_product_df=maven["product"],
    )

    assert isinstance(recommendations_df, pd.DataFrame)
    assert len(recommendations_df) == 5

    assert list(recommendations_df["RecommendationID"]) == [1, 2, 3, 4, 5]

    assert recommendations_df["Finding"].notna().all()
    assert recommendations_df["Recommendation"].notna().all()
    assert recommendations_df["Metric"].notna().all()

    assert set(recommendations_df["Area"]) == {
        "Gross Margin",
        "Customer Profitability",
        "Seller Profitability",
        "Pipeline Visibility",
        "Pipeline Prioritization",
    }

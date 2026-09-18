from pathlib import Path

import pandas as pd

from src.reporting.recommendations import (
    build_customer_profitability_recommendation,
    build_management_recommendations,
    build_margin_recommendation,
    build_pipeline_prioritization_recommendation,
    build_pipeline_visibility_recommendation,
    build_seller_profitability_recommendation,
    export_management_recommendations,
)


def _executive_kpis():
    return {
        "gross_margin_pct": 11.43,
    }


def _category_df():
    return pd.DataFrame(
        {
            "ProductCategory": ["Bikes", "Components"],
            "GrossMarginPct": [8.0, 12.0],
        }
    )


def _adventureworks_product_df():
    return pd.DataFrame(
        {
            "ProductName": ["Product A", "Product B", "Product C", "Product D"],
            "Revenue": [500000, 400000, 300000, 100000],
            "GrossMarginPct": [4.0, 10.0, 12.0, 15.0],
        }
    )


def _customer_df():
    return pd.DataFrame(
        {
            "CustomerID": [1, 2, 3],
            "Revenue": [500000, 400000, 300000],
            "GrossProfit": [-1000, 50000, 25000],
        }
    )


def _seller_df():
    return pd.DataFrame(
        {
            "SalesPersonID": [1, 2],
            "SalesPersonFirstName": ["John", "Jane"],
            "SalesPersonLastName": ["Smith", "Doe"],
            "GrossProfit": [-1000, 5000],
            "GrossMarginPct": [-2.0, 10.0],
        }
    )


def _pipeline_df():
    return pd.DataFrame(
        {
            "is_open": [True, True, False],
            "close_date": [
                pd.NaT,
                pd.Timestamp("2026-12-31"),
                pd.NaT,
            ],
            "close_value": [
                100000,
                200000,
                50000,
            ],
        }
    )


def _regional_df():
    return pd.DataFrame(
        {
            "regional_office": ["West", "East", "Central"],
            "OpportunityCount": [3000, 2000, 1500],
            "WinRatePct": [50.0, 65.0, 55.0],
        }
    )


def _maven_product_df():
    return pd.DataFrame(
        {
            "product_standardized": [
                "GTX Pro",
                "MG Advanced",
                "GTX Basic",
            ],
            "CloseValue": [5000000, 3000000, 1000000],
        }
    )


def test_margin_recommendation_uses_executive_kpi_dictionary():
    result = build_margin_recommendation(
        _executive_kpis(),
        _category_df(),
        _adventureworks_product_df(),
    )

    assert result["Area"] == "Gross Margin"
    assert result["Priority"] == "High"
    assert "Bikes" in result["Finding"]


def test_customer_profitability_recommendation_detects_loss_making_customer():
    result = build_customer_profitability_recommendation(
        _customer_df(),
        top_n=3,
    )

    assert result["Area"] == "Customer Profitability"
    assert result["Priority"] == "High"
    assert result["Metric"] == "1 / 3"


def test_seller_profitability_recommendation_uses_real_seller_columns():
    result = build_seller_profitability_recommendation(
        _seller_df(),
    )

    assert result["Area"] == "Seller Profitability"
    assert result["Priority"] == "High"
    assert "John Smith" in result["Finding"]


def test_pipeline_visibility_recommendation_detects_incomplete_open_pipeline():
    result = build_pipeline_visibility_recommendation(
        _pipeline_df(),
    )

    assert result["Area"] == "Pipeline Visibility"
    assert result["Priority"] == "Medium/High"
    assert result["Metric"] == "1"


def test_pipeline_prioritization_uses_maven_product_dataset():
    result = build_pipeline_prioritization_recommendation(
        _regional_df(),
        _maven_product_df(),
    )

    assert result["Area"] == "Pipeline Prioritization"
    assert "West" in result["Finding"]
    assert "GTX Pro" in result["Finding"]
    assert result["Metric"] == "3,000 opportunities"


def test_build_management_recommendations_returns_five_rows():
    result = build_management_recommendations(
        _executive_kpis(),
        _category_df(),
        _adventureworks_product_df(),
        _customer_df(),
        _seller_df(),
        _pipeline_df(),
        _regional_df(),
        _maven_product_df(),
    )

    assert len(result) == 5
    assert list(result["RecommendationID"]) == [1, 2, 3, 4, 5]
    assert set(result["Area"]) == {
        "Gross Margin",
        "Customer Profitability",
        "Seller Profitability",
        "Pipeline Visibility",
        "Pipeline Prioritization",
    }


def test_export_management_recommendations_creates_csv(tmp_path):
    recommendations = pd.DataFrame(
        [
            {
                "RecommendationID": 1,
                "Priority": "High",
                "Area": "Gross Margin",
                "Finding": "Test finding",
                "Recommendation": "Test recommendation",
                "Metric": "11.43%",
            }
        ]
    )

    output_path = export_management_recommendations(
        recommendations,
        output_directory=tmp_path,
    )

    assert output_path == Path(tmp_path) / "management_recommendations.csv"
    assert output_path.exists()

    exported = pd.read_csv(output_path)

    assert len(exported) == 1
    assert exported.loc[0, "Area"] == "Gross Margin"

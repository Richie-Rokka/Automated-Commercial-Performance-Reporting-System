from src.adventureworks.connection import create_database_engine

from src.adventureworks.extract import (
    extract_commercial_data,
    extract_historical_costs,
    extract_current_product_costs,
)

from src.adventureworks.transform import (
    calculate_commercial_metrics,
)


engine = create_database_engine()

commercial_data_df = extract_commercial_data(engine)

historical_cost_df = extract_historical_costs(engine)

current_cost_df = extract_current_product_costs(engine)


reporting_df = calculate_commercial_metrics(
    commercial_data_df,
    historical_cost_df,
    current_cost_df,
)


print("Reporting data:", reporting_df.shape)
print()
print(
    reporting_df[
        [
            "SalesOrderDetailID",
            "ProductID",
            "Revenue",
            "ReportingUnitCost",
            "Cost",
            "GrossProfit",
            "GrossMarginPct",
        ]
    ].head()
)
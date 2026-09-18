from src.adventureworks.connection import (
    create_database_engine
)

from src.adventureworks.extract import (
    extract_commercial_data,
    extract_historical_costs,
    extract_current_product_costs,
)

from src.adventureworks.transform import (
    calculate_commercial_metrics,
)

from src.adventureworks.datasets import (
    build_reporting_datasets,
)


engine = create_database_engine()

commercial_data_df = extract_commercial_data(
    engine
)

historical_cost_df = extract_historical_costs(
    engine
)

current_cost_df = extract_current_product_costs(
    engine
)

reporting_df = calculate_commercial_metrics(
    commercial_data_df,
    historical_cost_df,
    current_cost_df,
)

datasets = build_reporting_datasets(
    reporting_df
)


print()
print("EXECUTIVE KPIs")
print(datasets["executive_kpis"])

print()
print("MONTHLY PERFORMANCE")
print(
    datasets["monthly_performance"].shape
)
print(
    datasets["monthly_performance"].head()
)

print()
print("CATEGORY PERFORMANCE")
print(
    datasets["category_performance"]
)

print()
print("PRODUCT PERFORMANCE")
print(
    datasets["product_performance"].shape
)
print(
    datasets["product_performance"].head()
)

print()
print("CUSTOMER PERFORMANCE")
print(
    datasets["customer_performance"].shape
)
print(
    datasets["customer_performance"].head()
)

print()
print("SELLER PERFORMANCE")
print(
    datasets["seller_performance"].shape
)
print(
    datasets["seller_performance"]
)

print()
print("KEY OBSERVATIONS")

for observation in datasets["key_observations"]:
    print(f"• {observation}")
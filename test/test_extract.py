from src.adventureworks.connection import create_database_engine
from src.adventureworks.extract import (
    extract_sales_detail,
    extract_commercial_data,
    extract_historical_costs,
    extract_current_product_costs,
)


engine = create_database_engine()

sales_detail_df = extract_sales_detail(engine)

commercial_data_df = extract_commercial_data(engine)

historical_cost_df = extract_historical_costs(engine)

current_cost_df = extract_current_product_costs(engine)


print("Rows:", len(sales_detail_df))
print("Columns:", len(sales_detail_df.columns))
print()
print("Sales detail:", sales_detail_df.shape)
print(sales_detail_df.head())
print("Commercial data:", commercial_data_df.shape)
print("Historical costs:", historical_cost_df.shape)
print("Current product costs:", current_cost_df.shape)
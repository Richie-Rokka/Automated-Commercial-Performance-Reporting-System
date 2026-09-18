from src.adventureworks.connection import create_database_engine

from src.adventureworks.extract import (
    extract_commercial_data,
    extract_historical_costs,
    extract_current_product_costs,
)

from src.adventureworks.transform import (
    calculate_commercial_metrics,
)

from src.adventureworks.validate import (
    validate_reporting_data,
)


EXPECTED_ROW_COUNT = 121317


engine = create_database_engine()

commercial_data_df = extract_commercial_data(engine)

historical_cost_df = extract_historical_costs(engine)

current_cost_df = extract_current_product_costs(engine)

reporting_df = calculate_commercial_metrics(
    commercial_data_df,
    historical_cost_df,
    current_cost_df,
)

validate_reporting_data(
    reporting_df,
    EXPECTED_ROW_COUNT,
)
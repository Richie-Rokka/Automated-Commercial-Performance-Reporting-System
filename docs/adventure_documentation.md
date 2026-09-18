# AdventureWorks Reporting Pipeline --- Complete Implementation Guide

**Project:** Automated Commercial Performance Reporting System\
**Source:** Microsoft AdventureWorks2022\
**Pipeline:** SQL Server → Python → pandas → Excel\
**Primary implementation:** `src/generate_adventureworks_report.py`\
**Development notebook:** `01_python_environment_check.ipynb`\
**Output:** `reports/adventureworks_commercial_performance_report.xlsx`

------------------------------------------------------------------------

## 1. Purpose of This Document

This document is the **implementation and learning guide** for the
AdventureWorks portion of the Automated Commercial Performance Reporting
System.

It is intentionally different from a project summary.

It records:

-   why the AdventureWorks source was selected;
-   the architecture used;
-   environment and connection setup;
-   database discovery;
-   source-table selection;
-   source profiling;
-   relationship controls;
-   sales-grain validation;
-   historical-cost investigation;
-   the business rules used for cost and profitability;
-   the SQL extraction logic;
-   the Python transformation logic;
-   the reporting datasets;
-   the Excel-generation logic;
-   formatting;
-   chart creation;
-   final saved-workbook validation;
-   errors encountered and how they were resolved;
-   the complete implementation sequence;
-   what each major piece of code does;
-   how the pattern will be reused for the next source.

The goal is that another analyst---or the future version of the
project---can use this document to understand and reproduce the pipeline
rather than merely seeing the final result.

------------------------------------------------------------------------

# 2. Business Objective

The objective of the AdventureWorks phase is to demonstrate a repeatable
**commercial performance reporting automation process**.

The process should answer:

1.  Can Python reliably access the source system?
2.  Can the relevant commercial data be extracted at the correct grain?
3.  Can historical product cost be applied correctly?
4.  Can revenue, cost, gross profit, and gross margin be calculated
    reliably?
5.  Can the resulting data be organized into useful management reporting
    datasets?
6.  Can Python automatically produce a professional Excel report?
7.  Can the saved report be reopened and validated automatically?

This phase is about **reporting automation**, not exhaustive database
testing.

------------------------------------------------------------------------

# 3. Project Scope

## 3.1 Included

The AdventureWorks reporting pipeline includes:

1.  SQL Server connectivity.
2.  Sales extraction.
3.  Commercial dimension enrichment.
4.  Historical product-cost matching.
5.  Controlled cost fallback.
6.  Financial calculations.
7.  Risk-based validation.
8.  Executive KPIs.
9.  Monthly performance.
10. Category performance.
11. Product performance.
12. Customer performance.
13. Seller performance.
14. Excel workbook generation.
15. Excel presentation formatting.
16. Executive trend chart.
17. Final saved-artifact validation.

## 3.2 Deliberately Excluded

The following were intentionally not added:

-   exhaustive foreign-key testing across every AdventureWorks table;
-   a large automated insight/commentary engine;
-   unnecessary analytical dimensions;
-   premature Maven CRM integration;
-   a data warehouse or semantic layer for this source;
-   additional dashboard tooling beyond the completed Excel report.

The governing principle is:

> Validate and analyze what is necessary to make the automated report
> trustworthy. Do not expand the project simply because additional tests
> or analytics are technically possible.

------------------------------------------------------------------------

# 4. High-Level Architecture

The completed architecture is:

``` text
                    ┌──────────────────────────┐
                    │ AdventureWorks2022       │
                    │ SQL Server Express       │
                    └────────────┬─────────────┘
                                 │
                                 │ SQL
                                 ▼
                    ┌──────────────────────────┐
                    │ Python / SQLAlchemy      │
                    │ pyodbc / pandas          │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Commercial Data          │
                    │ Extraction               │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Business Calculations    │
                    │ Revenue / Cost / GP / GM │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Risk-Based Validation    │
                    │ Financial Reconciliation │
                    └────────────┬─────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────────┐
        │ Reporting Data Package                          │
        │ Executive / Monthly / Category / Product       │
        │ Customer / Seller                              │
        └────────────────────────┬───────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ openpyxl                 │
                    │ Excel generation         │
                    │ Formatting + Chart       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Saved Excel Report        │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Final Workbook Validation │
                    └──────────────────────────┘
```

The architecture separates:

-   **source access**;
-   **business logic**;
-   **validation**;
-   **report-data construction**;
-   **presentation**.

This prevents Excel formatting code from becoming responsible for
business calculations.

------------------------------------------------------------------------

# 5. Project Structure

The project began with:

``` text
C:\Data Analytics\Automated Commercial Performance Reporting System
│
├── .venv
├── data
│   └── raw
│       ├── adventureworks
│       └── maven_crm
└── 01_python_environment_check.ipynb
```

The AdventureWorks reusable reporting script was subsequently created
at:

``` text
src/
└── generate_adventureworks_report.py
```

The generated report is:

``` text
reports/
└── adventureworks_commercial_performance_report.xlsx
```

The completed documentation is:

``` text
doc/
└── adventure_documentation.md
```

------------------------------------------------------------------------

# 6. Environment Setup

The Python virtual environment was used so project dependencies remain
isolated from the global Python installation.

The key packages used were:

``` text
pandas
pyodbc
SQLAlchemy
openpyxl
matplotlib
```

The relevant verified versions included:

``` text
pandas 3.0.5
pyodbc 5.3.0
SQLAlchemy 2.0.52
```

The database connection used:

``` text
SQL Server Express
localhost\SQLEXPRESS
AdventureWorks2022
ODBC Driver 18
```

------------------------------------------------------------------------

# 7. SQL Server Connection

## 7.1 Initial pyodbc connection

The initial connection test used:

``` python
import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=AdventureWorks2022;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

connection = pyodbc.connect(
    connection_string,
    timeout=5
)

print("Connection successful.")
```

### What this code does

`pyodbc` allows Python to communicate with ODBC-compatible databases.

The connection string specifies:

-   `DRIVER` --- the ODBC driver;
-   `SERVER` --- SQL Server instance;
-   `DATABASE` --- target database;
-   `Trusted_Connection=yes` --- use Windows authentication;
-   `TrustServerCertificate=yes` --- accept the local SQL Server
    certificate.

The connection test establishes that Python can reach the database
before the reporting logic is attempted.

------------------------------------------------------------------------

# 8. SQLAlchemy Connection

For the reporting pipeline, SQLAlchemy was used as the database engine
layer.

``` python
from sqlalchemy import create_engine
from urllib.parse import quote_plus

connection_string = quote_plus(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=AdventureWorks2022;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={connection_string}"
)

print("SQLAlchemy engine created successfully.")
```

## Why SQLAlchemy?

The engine provides a reusable database connection interface that works
cleanly with pandas.

The reporting pipeline can then use:

``` python
pd.read_sql_query(query, engine)
```

instead of manually opening and closing individual database cursors for
every query.

------------------------------------------------------------------------

# 9. Database Identity Validation

Before extracting reporting data, the database identity was verified:

``` python
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("""
            SELECT
                @@SERVERNAME AS ServerName,
                DB_NAME() AS DatabaseName;
        """)
    )

    row = result.fetchone()

print("Server:", row.ServerName)
print("Database:", row.DatabaseName)
```

This confirmed that the process was connected to:

``` text
AdventureWorks2022
```

This is a simple but valuable control. A reporting process should not
silently execute against the wrong database.

------------------------------------------------------------------------

# 10. Source-System Discovery

The relevant source tables were identified from the AdventureWorks
schema.

## 10.1 Transaction tables

### Sales.SalesOrderHeader

Provides order-level attributes:

``` text
SalesOrderID
OrderDate
CustomerID
SalesPersonID
TerritoryID
Status
OnlineOrderFlag
SubTotal
TaxAmt
Freight
TotalDue
...
```

### Sales.SalesOrderDetail

Provides sales-line attributes:

``` text
SalesOrderID
SalesOrderDetailID
OrderQty
ProductID
SpecialOfferID
UnitPrice
UnitPriceDiscount
LineTotal
...
```

The reporting grain is:

> one row per SalesOrderDetailID.

------------------------------------------------------------------------

# 11. Supporting Dimensions

The reporting model uses:

``` text
Sales.Customer
Person.Person
Sales.SalesPerson
Sales.SalesTerritory
Production.Product
Production.ProductSubcategory
Production.ProductCategory
Production.ProductCostHistory
```

Their reporting roles are:

  Table                  Role
  ---------------------- ----------------------------
  Sales.Customer         Customer and account
  Person.Person          Customer/salesperson names
  Sales.SalesPerson      Salesperson
  Sales.SalesTerritory   Territory
  Production.Product     Product
  ProductSubcategory     Product hierarchy
  ProductCategory        Product hierarchy
  ProductCostHistory     Historical product cost

------------------------------------------------------------------------

# 12. Source Row Counts

The source was profiled before building the report.

Known populations included:

  Table                         Rows
  ------------------------ ---------
  Sales.SalesOrderHeader      31,465
  Sales.SalesOrderDetail     121,317
  Sales.Customer              19,820
  Production.Product             504
  Sales.SalesPerson               17
  Sales.SalesTerritory            10
  ProductSubcategory              37
  ProductCategory                  4
  Person.Person               19,972

The most important population for the commercial report is:

``` text
Sales.SalesOrderDetail = 121,317
```

------------------------------------------------------------------------

# 13. Reporting Grain

The central reporting grain is:

``` text
one row per SalesOrderDetailID
```

This matters because aggregation at the wrong grain can double-count
revenue or cost.

The grain control confirmed:

``` text
SalesOrderDetailID count = 121,317
Unique SalesOrderDetailID = 121,317
```

Therefore:

``` text
Duplicate sales lines = 0
```

------------------------------------------------------------------------

# 14. Risk-Based Relationship Validation

The project intentionally used targeted relationship controls.

## 14.1 Sales detail → order header

Control:

``` text
SalesOrderDetail.SalesOrderID
        ↓
SalesOrderHeader.SalesOrderID
```

Result:

``` text
0 orphan rows
```

## 14.2 Sales detail → product

``` text
SalesOrderDetail.ProductID
        ↓
Production.Product.ProductID
```

Result:

``` text
0 orphan rows
```

## 14.3 Order → customer

``` text
SalesOrderHeader.CustomerID
        ↓
Sales.Customer.CustomerID
```

Result:

``` text
0 orphan rows
```

## 14.4 Customer → person

``` text
Sales.Customer.PersonID
        ↓
Person.Person.BusinessEntityID
```

Result:

``` text
0 orphan rows
```

## 14.5 Order → salesperson

``` text
SalesOrderHeader.SalesPersonID
        ↓
Sales.SalesPerson.BusinessEntityID
```

Result:

``` text
0 orphan rows
```

## 14.6 Salesperson relationships

Salesperson relationships to Employee and Person were also checked.

Results:

``` text
SalesPerson → Employee = 0 orphan rows
SalesPerson → Person    = 0 orphan rows
```

Additional relationships such as ShipMethod, CreditCard, CurrencyRate
and addresses were not tested because they were not required by the
final report.

------------------------------------------------------------------------

# 15. Sales Detail Extraction

The initial sales-detail query was:

``` python
def extract_sales_detail(engine):
    query = """
        SELECT
            soh.SalesOrderID,
            sod.SalesOrderDetailID,
            soh.OrderDate,
            soh.CustomerID,
            soh.SalesPersonID,
            soh.TerritoryID,
            sod.ProductID,
            sod.OrderQty,
            sod.UnitPrice,
            sod.UnitPriceDiscount,
            sod.LineTotal
        FROM Sales.SalesOrderHeader AS soh
        INNER JOIN Sales.SalesOrderDetail AS sod
            ON soh.SalesOrderID = sod.SalesOrderID;
    """

    sales_detail_df = pd.read_sql_query(
        query,
        engine
    )

    return sales_detail_df
```

The result:

``` text
121,317 rows
11 columns
```

The Python row count matched the source population:

``` text
121,317 vs 121,317
Difference = 0
```

------------------------------------------------------------------------

# 16. Commercial Data Extraction

The business-facing commercial query enriched the sales line with
customer, salesperson, territory and product information.

``` python
def extract_commercial_data(engine):
    query = """
        SELECT
            soh.SalesOrderID,
            sod.SalesOrderDetailID,
            soh.OrderDate,
            soh.CustomerID,
            c.AccountNumber,
            cp.FirstName,
            cp.LastName,
            soh.SalesPersonID,
            sp.FirstName AS SalesPersonFirstName,
            sp.LastName AS SalesPersonLastName,
            soh.TerritoryID,
            st.Name AS TerritoryName,
            st.CountryRegionCode,
            st.[Group] AS TerritoryGroup,
            sod.ProductID,
            prod.Name AS ProductName,
            ps.Name AS ProductSubcategory,
            pc.Name AS ProductCategory,
            sod.OrderQty,
            sod.UnitPrice,
            sod.UnitPriceDiscount,
            sod.LineTotal AS Revenue
        FROM Sales.SalesOrderHeader AS soh
        INNER JOIN Sales.SalesOrderDetail AS sod
            ON soh.SalesOrderID = sod.SalesOrderID
        INNER JOIN Sales.Customer AS c
            ON soh.CustomerID = c.CustomerID
        LEFT JOIN Person.Person AS cp
            ON c.PersonID = cp.BusinessEntityID
        LEFT JOIN Sales.SalesPerson AS sp_base
            ON soh.SalesPersonID = sp_base.BusinessEntityID
        LEFT JOIN Person.Person AS sp
            ON sp_base.BusinessEntityID = sp.BusinessEntityID
        INNER JOIN Sales.SalesTerritory AS st
            ON soh.TerritoryID = st.TerritoryID
        INNER JOIN Production.Product AS prod
            ON sod.ProductID = prod.ProductID
        LEFT JOIN Production.ProductSubcategory AS ps
            ON prod.ProductSubcategoryID = ps.ProductSubcategoryID
        LEFT JOIN Production.ProductCategory AS pc
            ON ps.ProductCategoryID = pc.ProductCategoryID;
    """

    commercial_data_df = pd.read_sql_query(
        query,
        engine
    )

    return commercial_data_df
```

Result:

``` text
121,317 rows
22 columns
```

The query preserves the sales-line grain.

------------------------------------------------------------------------

# 17. Historical Product Cost

## 17.1 Why current StandardCost is insufficient

`Production.Product.StandardCost` represents the product's current
standard cost.

The report spans:

``` text
2011-05-31 → 2014-06-30
```

Using today's/current cost for every historical transaction could
therefore distort historical gross profit.

The appropriate source is:

``` text
Production.ProductCostHistory
```

------------------------------------------------------------------------

# 18. First Historical-Cost Attempt

The initial effective-date condition used:

``` sql
OrderDate >= StartDate
AND OrderDate < EndDate
```

That produced:

``` text
121,237 matched historical lines
80 missing lines
```

The investigation showed that the boundary condition excluded
transactions occurring on an EndDate.

------------------------------------------------------------------------

# 19. Correct Historical-Cost Rule

The corrected rule was:

``` sql
OrderDate >= StartDate
AND (
    EndDate IS NULL
    OR OrderDate <= EndDate
)
```

This produced:

``` text
121,253 historical matches
64 unmatched rows
0 unresolved after fallback
```

This was an important business-rule correction rather than a cosmetic
code change.

------------------------------------------------------------------------

# 20. Historical-Cost Extraction Code

``` python
def extract_historical_costs(engine):
    query = """
        SELECT
            sod.SalesOrderDetailID,
            sod.ProductID,
            soh.OrderDate,
            pch.StandardCost AS UnitCost
        FROM Sales.SalesOrderHeader AS soh
        INNER JOIN Sales.SalesOrderDetail AS sod
            ON soh.SalesOrderID = sod.SalesOrderID
        LEFT JOIN Production.ProductCostHistory AS pch
            ON sod.ProductID = pch.ProductID
            AND soh.OrderDate >= pch.StartDate
            AND (
                pch.EndDate IS NULL
                OR soh.OrderDate <= pch.EndDate
            );
    """

    historical_cost_df = pd.read_sql_query(
        query,
        engine
    )

    return historical_cost_df
```

------------------------------------------------------------------------

# 21. Current-Cost Fallback

The controlled fallback source is:

``` python
def extract_current_product_costs(engine):
    query = """
        SELECT
            ProductID,
            StandardCost AS CurrentStandardCost
        FROM Production.Product;
    """

    current_cost_df = pd.read_sql_query(
        query,
        engine
    )

    return current_cost_df
```

The fallback is not intended to replace historical costing.

It exists only for historical transactions for which no historical cost
record exists.

------------------------------------------------------------------------

# 22. Fallback Validation

The final result contained:

``` text
Historical cost rows: 121,253
Fallback rows: 64
Unresolved rows: 0
```

The 64 fallback rows involved:

``` text
25 products
```

The current standard cost was compared with the latest historical cost
for those products.

The values matched for the fallback population, providing support for
the controlled fallback approach.

------------------------------------------------------------------------

# 23. Commercial Calculation Layer

The calculation function is:

``` python
def calculate_commercial_metrics(
    commercial_data_df,
    historical_cost_df,
    current_cost_df
):
    reporting_df = commercial_data_df.merge(
        historical_cost_df[
            [
                "SalesOrderDetailID",
                "UnitCost"
            ]
        ],
        on="SalesOrderDetailID",
        how="left"
    )

    reporting_df = reporting_df.merge(
        current_cost_df,
        on="ProductID",
        how="left"
    )

    reporting_df["ReportingUnitCost"] = (
        reporting_df["UnitCost"]
        .fillna(
            reporting_df["CurrentStandardCost"]
        )
    )

    reporting_df["Cost"] = (
        reporting_df["OrderQty"]
        * reporting_df["ReportingUnitCost"]
    )

    reporting_df["GrossProfit"] = (
        reporting_df["Revenue"]
        - reporting_df["Cost"]
    )

    reporting_df["GrossMarginPct"] = (
        reporting_df["GrossProfit"]
        / reporting_df["Revenue"]
    ) * 100

    return reporting_df
```

------------------------------------------------------------------------

# 24. Understanding the Calculation Code

## Merge historical cost

``` python
reporting_df = commercial_data_df.merge(
    historical_cost_df[["SalesOrderDetailID", "UnitCost"]],
    on="SalesOrderDetailID",
    how="left"
)
```

The `SalesOrderDetailID` is the stable transaction-line key.

A `left` join preserves every sales line even if historical cost is
missing.

## Merge fallback cost

``` python
reporting_df = reporting_df.merge(
    current_cost_df,
    on="ProductID",
    how="left"
)
```

This adds the current product standard cost.

## Select reporting cost

``` python
reporting_df["ReportingUnitCost"] = (
    reporting_df["UnitCost"]
    .fillna(reporting_df["CurrentStandardCost"])
)
```

`fillna()` means:

> use historical cost when available; otherwise use current standard
> cost.

## Calculate cost

``` python
reporting_df["Cost"] = (
    reporting_df["OrderQty"]
    * reporting_df["ReportingUnitCost"]
)
```

## Calculate gross profit

``` python
reporting_df["GrossProfit"] = (
    reporting_df["Revenue"]
    - reporting_df["Cost"]
)
```

## Calculate margin

``` python
reporting_df["GrossMarginPct"] = (
    reporting_df["GrossProfit"]
    / reporting_df["Revenue"]
) * 100
```

The value is stored in Python as a percentage-style number such as:

``` text
11.4321
```

When writing to Excel, detail-sheet formatting converts this to the
Excel decimal representation:

``` text
0.114321
```

and applies:

``` text
0.00%
```

------------------------------------------------------------------------

# 25. Financial Validation

Financial validation was implemented as:

``` python
def validate_financial_calculations(reporting_df):
    total_revenue = reporting_df["Revenue"].sum()
    total_cost = reporting_df["Cost"].sum()
    total_gross_profit = reporting_df["GrossProfit"].sum()

    expected_gross_profit = (
        total_revenue
        - total_cost
    )

    gross_profit_difference = abs(
        total_gross_profit
        - expected_gross_profit
    )

    unresolved_costs = (
        reporting_df["ReportingUnitCost"]
        .isna()
        .sum()
    )

    fallback_count = (
        reporting_df["UnitCost"]
        .isna()
        .sum()
    )

    print()
    print("FINANCIAL VALIDATION")
    print("-" * 40)

    print("Revenue:", total_revenue)
    print("Cost:", total_cost)
    print("Gross Profit:", total_gross_profit)
    print(
        "Gross Profit reconciliation difference:",
        gross_profit_difference
    )
    print("Fallback cost rows:", fallback_count)
    print("Unresolved cost rows:", unresolved_costs)

    assert gross_profit_difference < 0.01, (
        "Gross Profit reconciliation failed."
    )

    assert unresolved_costs == 0, (
        "Unresolved product costs detected."
    )

    print("Financial validation: PASS")
```

------------------------------------------------------------------------

# 26. Financial Validation Results

Final results:

``` text
Revenue: 109846381.39988798
Cost: 97288600.8008
Gross Profit: 12557780.599088002
Gross Profit reconciliation difference: 1.862645149230957e-08
Fallback cost rows: 64
Unresolved cost rows: 0
Financial validation: PASS
```

Business presentation:

  KPI                        Result
  -------------- ------------------
  Revenue          \$109,846,381.40
  Cost              \$97,288,600.80
  Gross Profit      \$12,557,780.60
  Gross Margin               11.43%
  Sales lines               121,317
  Units sold                274,914
  Customers                  19,119
  Products                      266

------------------------------------------------------------------------

# 27. Final Reporting Dataset

The business-facing dataset contains:

``` text
SalesOrderID
SalesOrderDetailID
OrderDate
CustomerID
AccountNumber
FirstName
LastName
SalesPersonID
SalesPersonFirstName
SalesPersonLastName
TerritoryID
TerritoryName
CountryRegionCode
TerritoryGroup
ProductID
ProductName
ProductSubcategory
ProductCategory
OrderQty
UnitPrice
UnitPriceDiscount
Revenue
ReportingUnitCost
Cost
GrossProfit
GrossMarginPct
```

Final population:

``` text
121,317 rows
28 columns
```

------------------------------------------------------------------------

# 28. Monthly Reporting Dataset

A reporting month was created from `OrderDate`:

``` python
commercial_reporting_df["OrderMonth"] = (
    commercial_reporting_df["OrderDate"]
    .dt.to_period("M")
)
```

Monthly aggregation:

``` python
monthly_performance_df = (
    commercial_reporting_df
    .groupby("OrderMonth")
    .agg(
        Revenue=("Revenue", "sum"),
        Cost=("Cost", "sum"),
        GrossProfit=("GrossProfit", "sum"),
        SalesLines=("SalesOrderDetailID", "count")
    )
    .reset_index()
)

monthly_performance_df["GrossMarginPct"] = (
    monthly_performance_df["GrossProfit"]
    / monthly_performance_df["Revenue"]
) * 100
```

The result contains:

``` text
38 monthly periods
```

The reporting period is:

``` text
2011-05-31 → 2014-06-30
```

------------------------------------------------------------------------

# 29. Month-over-Month Measures

The dataset also calculated:

``` python
monthly_performance_df["RevenueChangePct"] = (
    monthly_performance_df["Revenue"].pct_change()
) * 100

monthly_performance_df["GrossProfitChangePct"] = (
    monthly_performance_df["GrossProfit"].pct_change()
) * 100

monthly_performance_df["MarginChangePts"] = (
    monthly_performance_df["GrossMarginPct"].diff()
)
```

A final-period flag was also created:

``` python
monthly_performance_df["IsFinalPeriod"] = (
    monthly_performance_df["OrderMonth"]
    == monthly_performance_df["OrderMonth"].max()
)
```

This is important because June 2014 is a partial/final period in the
source and should not automatically be interpreted as a normal
full-month decline.

------------------------------------------------------------------------

# 30. Executive KPI Dataset

The executive KPI dictionary is:

``` python
executive_kpis = {
    "report_start_date": commercial_reporting_df["OrderDate"].min(),
    "report_end_date": commercial_reporting_df["OrderDate"].max(),
    "revenue": commercial_reporting_df["Revenue"].sum(),
    "cost": commercial_reporting_df["Cost"].sum(),
    "gross_profit": commercial_reporting_df["GrossProfit"].sum(),
    "gross_margin_pct": (
        commercial_reporting_df["GrossProfit"].sum()
        / commercial_reporting_df["Revenue"].sum()
    ) * 100,
    "sales_lines": commercial_reporting_df["SalesOrderDetailID"].nunique(),
    "units_sold": commercial_reporting_df["OrderQty"].sum(),
    "customers": commercial_reporting_df["CustomerID"].nunique(),
    "products": commercial_reporting_df["ProductID"].nunique(),
}
```

------------------------------------------------------------------------

# 31. Category Performance

The category dataset is created with:

``` python
category_performance_df = (
    commercial_reporting_df
    .groupby("ProductCategory")
    .agg(
        Revenue=("Revenue", "sum"),
        Cost=("Cost", "sum"),
        GrossProfit=("GrossProfit", "sum"),
        UnitsSold=("OrderQty", "sum"),
        SalesLines=("SalesOrderDetailID", "count"),
        Products=("ProductID", "nunique")
    )
    .reset_index()
)

category_performance_df["GrossMarginPct"] = (
    category_performance_df["GrossProfit"]
    / category_performance_df["Revenue"]
) * 100

category_performance_df = category_performance_df.sort_values(
    "Revenue",
    ascending=False
)
```

Final categories:

  Category         Revenue   Gross Profit   Margin
  ------------- ---------- -------------- --------
  Bikes           \$94.65M       \$10.52M   11.11%
  Components      \$11.80M        \$1.03M    8.76%
  Clothing         \$2.12M        \$0.37M   17.44%
  Accessories      \$1.27M        \$0.63M   49.88%

------------------------------------------------------------------------

# 32. Product Performance

The product dataset is:

``` python
product_performance_df = (
    commercial_reporting_df
    .groupby(
        ["ProductID", "ProductName"]
    )
    .agg(
        Revenue=("Revenue", "sum"),
        Cost=("Cost", "sum"),
        GrossProfit=("GrossProfit", "sum"),
        UnitsSold=("OrderQty", "sum"),
        SalesLines=("SalesOrderDetailID", "count")
    )
    .reset_index()
)

product_performance_df["GrossMarginPct"] = (
    product_performance_df["GrossProfit"]
    / product_performance_df["Revenue"]
) * 100

product_performance_df = product_performance_df.sort_values(
    "Revenue",
    ascending=False
)
```

The full product dataset contains:

``` text
266 products
```

The Excel report displays:

``` text
Top 15 products by revenue
```

------------------------------------------------------------------------

# 33. Customer Performance

Customer aggregation:

``` python
customer_performance_df = (
    commercial_reporting_df
    .groupby(
        [
            "CustomerID",
            "AccountNumber",
            "FirstName",
            "LastName"
        ]
    )
    .agg(
        Revenue=("Revenue", "sum"),
        Cost=("Cost", "sum"),
        GrossProfit=("GrossProfit", "sum"),
        UnitsSold=("OrderQty", "sum"),
        SalesLines=("SalesOrderDetailID", "count"),
        ProductsPurchased=("ProductID", "nunique")
    )
    .reset_index()
)

customer_performance_df["GrossMarginPct"] = (
    customer_performance_df["GrossProfit"]
    / customer_performance_df["Revenue"]
) * 100

customer_performance_df = customer_performance_df.sort_values(
    "Revenue",
    ascending=False
)
```

Population:

``` text
19,119 customers
```

Excel display:

``` text
Top 15 customers by revenue
```

------------------------------------------------------------------------

# 34. Seller Performance

Seller aggregation:

``` python
seller_performance_df = (
    commercial_reporting_df
    .groupby(
        [
            "SalesPersonID",
            "SalesPersonFirstName",
            "SalesPersonLastName"
        ]
    )
    .agg(
        Revenue=("Revenue", "sum"),
        Cost=("Cost", "sum"),
        GrossProfit=("GrossProfit", "sum"),
        UnitsSold=("OrderQty", "sum"),
        SalesLines=("SalesOrderDetailID", "count"),
        Customers=("CustomerID", "nunique")
    )
    .reset_index()
)

seller_performance_df["GrossMarginPct"] = (
    seller_performance_df["GrossProfit"]
    / seller_performance_df["Revenue"]
) * 100

seller_performance_df = seller_performance_df.sort_values(
    "Revenue",
    ascending=False
)
```

Population:

``` text
17 sellers
```

------------------------------------------------------------------------

# 35. Report Data Package

The six reporting datasets were packaged together:

``` python
report_data = {
    "executive": executive_kpis,
    "monthly": monthly_performance_df,
    "category": category_performance_df,
    "product": product_performance_df,
    "customer": customer_performance_df,
    "seller": seller_performance_df,
}
```

This creates a clean boundary between:

``` text
Business calculations
```

and:

``` text
Excel presentation
```

------------------------------------------------------------------------

# 36. Excel Generation

The output directory is created with:

``` python
from pathlib import Path

report_output_dir = Path("reports")
report_output_dir.mkdir(exist_ok=True)

report_path = (
    report_output_dir
    / "adventureworks_commercial_performance_report.xlsx"
)
```

The workbook is created with:

``` python
from openpyxl import Workbook

workbook = Workbook()

if "Sheet" in workbook.sheetnames:
    del workbook["Sheet"]
```

The default blank worksheet is removed because the final report should
contain only intentional report sheets.

------------------------------------------------------------------------

# 37. Excel Worksheet Writer

The reusable writer function is:

``` python
def write_dataframe_to_sheet(
    workbook,
    sheet_name,
    dataframe,
    title=None
):
    """
    Write a pandas DataFrame into an Excel worksheet.

    If the worksheet already exists, use it.
    Otherwise, create it.
    """

    if sheet_name in workbook.sheetnames:
        worksheet = workbook[sheet_name]
    else:
        worksheet = workbook.create_sheet(sheet_name)

    for row in worksheet.iter_rows():
        for cell in row:
            cell.value = None

    current_row = 1

    if title:
        worksheet.cell(
            row=current_row,
            column=1,
            value=title
        )

        worksheet.cell(
            row=current_row,
            column=1
        ).font = Font(
            bold=True,
            size=14
        )

        current_row += 2

    for column_index, column_name in enumerate(
        dataframe.columns,
        start=1
    ):
        cell = worksheet.cell(
            row=current_row,
            column=column_index,
            value=column_name
        )

        cell.font = Font(bold=True)

        cell.alignment = Alignment(
            horizontal="center"
        )

    current_row += 1

    for row in dataframe.itertuples(
        index=False,
        name=None
    ):
        for column_index, value in enumerate(
            row,
            start=1
        ):
            worksheet.cell(
                row=current_row,
                column=column_index,
                value=value
            )

        current_row += 1

    for column_index in range(
        1,
        len(dataframe.columns) + 1
    ):
        column_letter = get_column_letter(
            column_index
        )

        worksheet.column_dimensions[
            column_letter
        ].width = 18

    worksheet.freeze_panes = (
        f"A{3 if title else 2}"
    )

    return worksheet
```

------------------------------------------------------------------------

# 38. Why the Writer Function Matters

Without a reusable function, every worksheet would require separate
Excel-writing code.

The function uses:

``` python
def
```

to define reusable behavior.

It accepts:

``` text
workbook
sheet_name
dataframe
title
```

The `if` statement determines whether to reuse or create a worksheet.

`enumerate()` provides both:

-   the numeric column position;
-   the column name.

`itertuples()` efficiently iterates through DataFrame rows.

`get_column_letter()` converts:

``` text
1 → A
2 → B
3 → C
```

and so on.

The function is deliberately limited to output mechanics. It does not
calculate revenue, cost, margin, or business KPIs.

------------------------------------------------------------------------

# 39. Pandas Period / Excel Compatibility Issue

The monthly dataset initially contained:

``` python
Period('2011-05', 'M')
```

openpyxl cannot write pandas `Period` objects directly into Excel.

The solution was:

``` python
monthly_report_df["OrderMonth"] = (
    monthly_report_df["OrderMonth"]
    .astype(str)
)
```

This produces:

``` text
2011-05
2011-06
...
2014-06
```

This is a presentation conversion, not a change to the underlying
business calculation.

------------------------------------------------------------------------

# 40. Detail Worksheet Formatting

The report uses a reusable formatter.

``` python
thin_border = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin")
)


def format_detail_sheet(
    worksheet,
    currency_columns=None,
    percentage_columns=None,
    integer_columns=None
):
    """
    Apply consistent presentation formatting to a report worksheet.
    """

    currency_columns = currency_columns or []
    percentage_columns = percentage_columns or []
    integer_columns = integer_columns or []

    worksheet["A1"].font = Font(
        bold=True,
        size=14
    )

    header_row = 3

    for cell in worksheet[header_row]:
        if cell.value is not None:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(
                horizontal="center"
            )
            cell.border = thin_border

    for row in worksheet.iter_rows(
        min_row=header_row + 1
    ):
        for cell in row:
            if cell.value is not None:
                cell.border = thin_border

    header_map = {
        cell.value: cell.column
        for cell in worksheet[header_row]
        if cell.value is not None
    }

    for column_name in currency_columns:
        if column_name in header_map:
            column_index = header_map[column_name]

            for row in range(
                header_row + 1,
                worksheet.max_row + 1
            ):
                worksheet.cell(
                    row=row,
                    column=column_index
                ).number_format = "$#,##0.00"

    for column_name in percentage_columns:
        if column_name in header_map:
            column_index = header_map[column_name]

            for row in range(
                header_row + 1,
                worksheet.max_row + 1
            ):
                cell = worksheet.cell(
                    row=row,
                    column=column_index
                )

                if isinstance(
                    cell.value,
                    (int, float)
                ):
                    cell.value = cell.value / 100

                cell.number_format = "0.00%"

    for column_name in integer_columns:
        if column_name in header_map:
            column_index = header_map[column_name]

            for row in range(
                header_row + 1,
                worksheet.max_row + 1
            ):
                worksheet.cell(
                    row=row,
                    column=column_index
                ).number_format = "#,##0"

    for column_index in range(
        1,
        worksheet.max_column + 1
    ):
        column_letter = get_column_letter(
            column_index
        )

        max_length = 0

        for row in worksheet.iter_rows(
            min_col=column_index,
            max_col=column_index
        ):
            for cell in row:
                if cell.value is not None:
                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )

        worksheet.column_dimensions[
            column_letter
        ].width = min(
            max(max_length + 2, 12),
            30
        )

    worksheet.freeze_panes = "A4"

    worksheet.auto_filter.ref = (
        f"A3:"
        f"{get_column_letter(worksheet.max_column)}"
        f"{worksheet.max_row}"
    )

    return worksheet
```

------------------------------------------------------------------------

# 41. Why Formatting Uses Header Names

The formatter creates:

``` python
header_map = {
    cell.value: cell.column
    for cell in worksheet[header_row]
}
```

This means the code asks:

> Where is the column called `GrossMarginPct`?

rather than assuming:

> GrossMarginPct is always column E.

This distinction became important during final validation.

The Monthly Performance worksheet actually has:

``` text
A = OrderMonth
B = Revenue
C = Cost
D = GrossProfit
E = SalesLines
F = GrossMarginPct
```

A hard-coded validation of `E4` incorrectly tested `SalesLines`.

The validation was corrected to find `GrossMarginPct` by header name.

------------------------------------------------------------------------

# 42. Applying Detail Formatting

Monthly:

``` python
format_detail_sheet(
    workbook["Monthly Performance"],
    currency_columns=[
        "Revenue",
        "Cost",
        "GrossProfit"
    ],
    percentage_columns=[
        "GrossMarginPct"
    ],
    integer_columns=[
        "SalesLines"
    ]
)
```

Category:

``` python
format_detail_sheet(
    workbook["Category Performance"],
    currency_columns=[
        "Revenue",
        "Cost",
        "GrossProfit"
    ],
    percentage_columns=[
        "GrossMarginPct"
    ],
    integer_columns=[
        "UnitsSold",
        "SalesLines",
        "Products"
    ]
)
```

Product:

``` python
format_detail_sheet(
    workbook["Product Performance"],
    currency_columns=[
        "Revenue",
        "Cost",
        "GrossProfit"
    ],
    percentage_columns=[
        "GrossMarginPct"
    ],
    integer_columns=[
        "ProductID",
        "UnitsSold",
        "SalesLines"
    ]
)
```

Customer:

``` python
format_detail_sheet(
    workbook["Customer Performance"],
    currency_columns=[
        "Revenue",
        "Cost",
        "GrossProfit"
    ],
    percentage_columns=[
        "GrossMarginPct"
    ],
    integer_columns=[
        "CustomerID",
        "UnitsSold",
        "SalesLines",
        "ProductsPurchased"
    ]
)
```

Seller:

``` python
format_detail_sheet(
    workbook["Seller Performance"],
    currency_columns=[
        "Revenue",
        "Cost",
        "GrossProfit"
    ],
    percentage_columns=[
        "GrossMarginPct"
    ],
    integer_columns=[
        "SalesPersonID",
        "UnitsSold",
        "SalesLines",
        "Customers"
    ]
)
```

------------------------------------------------------------------------

# 43. Executive Summary

The Executive Summary contains:

``` text
AUTOMATED COMMERCIAL PERFORMANCE REPORT
Reporting Period
Revenue
Cost
Gross Profit
Gross Margin %
Sales Lines
Units Sold
Customers
Products
```

The margin must be stored as an Excel decimal:

``` python
executive_sheet["B8"] = (
    executive_kpis["gross_margin_pct"] / 100
)

executive_sheet["B8"].number_format = "0.00%"
```

This is important because the Python KPI is stored as:

``` text
11.4321
```

while Excel's percentage representation expects:

``` text
0.114321
```

Otherwise Excel would display:

``` text
1143.21%
```

instead of:

``` text
11.43%
```

------------------------------------------------------------------------

# 44. Executive Trend Chart

The report contains one chart:

``` text
Monthly Revenue & Gross Profit Trend
```

The chart is built from the Monthly Performance worksheet.

``` python
from openpyxl.chart import LineChart, Reference

monthly_sheet = workbook["Monthly Performance"]
executive_sheet = workbook["Executive Summary"]

trend_chart = LineChart()

trend_chart.title = (
    "Monthly Revenue & Gross Profit Trend"
)

trend_chart.style = 2
trend_chart.height = 8
trend_chart.width = 18

revenue_data = Reference(
    monthly_sheet,
    min_col=2,
    min_row=3,
    max_row=41
)

gross_profit_data = Reference(
    monthly_sheet,
    min_col=4,
    min_row=3,
    max_row=41
)

month_labels = Reference(
    monthly_sheet,
    min_col=1,
    min_row=4,
    max_row=41
)

trend_chart.add_data(
    revenue_data,
    titles_from_data=True
)

trend_chart.add_data(
    gross_profit_data,
    titles_from_data=True
)

trend_chart.set_categories(
    month_labels
)

executive_sheet.add_chart(
    trend_chart,
    "D2"
)
```

The chart does not create new business logic.

It visualizes already-calculated reporting data.

------------------------------------------------------------------------

# 45. Why the Chart Uses Existing Data

The architecture intentionally keeps visualization downstream:

``` text
Source
  ↓
Business calculations
  ↓
Reporting dataset
  ↓
Chart
```

The chart should never independently calculate revenue or gross profit.

This reduces the risk of the workbook containing multiple definitions of
the same KPI.

------------------------------------------------------------------------

# 46. Workbook Save

The workbook is saved using:

``` python
workbook.save(REPORT_PATH)
```

The final output is:

``` text
reports\adventureworks_commercial_performance_report.xlsx
```

A file-lock issue occurred during development when the workbook was open
in Excel.

The resolution was simply to close the workbook before the Python
process attempted to overwrite it.

------------------------------------------------------------------------

# 47. Final Saved-Artifact Validation

The final validation was designed to reopen the actual `.xlsx` file.

This matters because:

> Successful Python execution does not automatically prove that the
> saved Excel artifact is correct.

The validation function starts with:

``` python
from openpyxl import load_workbook

saved_workbook = load_workbook(report_path)
```

It then checks the saved workbook itself.

------------------------------------------------------------------------

# 48. Final Workbook Validation Code

``` python
def validate_generated_workbook(report_path):
    """
    Validate the saved Excel report.

    The workbook is reopened from disk so that validation
    confirms the actual deliverable, not only the in-memory object.
    """

    from openpyxl import load_workbook

    print()
    print("=" * 60)
    print("FINAL WORKBOOK VALIDATION")
    print("=" * 60)

    assert report_path.exists(), (
        "Report file does not exist."
    )

    saved_workbook = load_workbook(report_path)

    expected_sheets = [
        "Executive Summary",
        "Monthly Performance",
        "Category Performance",
        "Product Performance",
        "Customer Performance",
        "Seller Performance"
    ]

    actual_sheets = saved_workbook.sheetnames

    assert actual_sheets == expected_sheets, (
        f"Worksheet validation failed.\n"
        f"Expected: {expected_sheets}\n"
        f"Actual: {actual_sheets}"
    )

    print("Worksheet structure: PASS")

    executive_sheet = saved_workbook[
        "Executive Summary"
    ]

    monthly_sheet = saved_workbook[
        "Monthly Performance"
    ]

    category_sheet = saved_workbook[
        "Category Performance"
    ]

    product_sheet = saved_workbook[
        "Product Performance"
    ]

    customer_sheet = saved_workbook[
        "Customer Performance"
    ]

    seller_sheet = saved_workbook[
        "Seller Performance"
    ]

    assert executive_sheet["A1"].value == (
        "AUTOMATED COMMERCIAL PERFORMANCE REPORT"
    )

    assert executive_sheet["A3"].value == (
        "Reporting Period"
    )

    assert abs(
        executive_sheet["B5"].value
        - 109846381.39988798
    ) < 0.01

    assert abs(
        executive_sheet["B8"].value
        - 0.1143212952402345
    ) < 0.000001

    print("Executive Summary: PASS")

    monthly_data_rows = (
        monthly_sheet.max_row - 3
    )

    assert monthly_data_rows == 38

    assert monthly_sheet["A4"].value == "2011-05"
    assert monthly_sheet["A41"].value == "2014-06"

    assert (
        monthly_sheet["B4"].number_format
        == "$#,##0.00"
    )

    monthly_header_map = {
        cell.value: cell.column
        for cell in monthly_sheet[3]
        if cell.value is not None
    }

    gross_margin_column = monthly_header_map[
        "GrossMarginPct"
    ]

    gross_margin_cell = monthly_sheet.cell(
        row=4,
        column=gross_margin_column
    )

    assert gross_margin_cell.number_format == "0.00%"

    print(
        "Monthly Gross Margin format:",
        gross_margin_cell.number_format
    )

    print("Monthly Performance: PASS")

    category_data_rows = (
        category_sheet.max_row - 3
    )

    assert category_data_rows == 4

    print("Category Performance: PASS")

    product_data_rows = (
        product_sheet.max_row - 3
    )

    assert product_data_rows == 15

    print("Product Performance: PASS")

    customer_data_rows = (
        customer_sheet.max_row - 3
    )

    assert customer_data_rows == 15

    print("Customer Performance: PASS")

    seller_data_rows = (
        seller_sheet.max_row - 3
    )

    assert seller_data_rows == 17

    print("Seller Performance: PASS")

    assert len(
        executive_sheet._charts
    ) == 1

    chart_title = (
        executive_sheet._charts[0]
        .title
        .tx
        .rich
        .p[0]
        .r[0]
        .t
    )

    assert chart_title == (
        "Monthly Revenue & Gross Profit Trend"
    )

    print("Executive trend chart: PASS")

    saved_workbook.close()

    print()
    print("FINAL WORKBOOK VALIDATION: PASS")
```

------------------------------------------------------------------------

# 49. Why `assert` Is Used

An assertion turns an expectation into an automated control.

For example:

``` python
assert monthly_data_rows == 38
```

means:

> If the saved workbook does not contain exactly 38 monthly data rows,
> stop the process and report failure.

Likewise:

``` python
assert unresolved_costs == 0
```

means:

> Never produce a report that silently contains unresolved reporting
> costs.

This is particularly important in automation because a human may not
inspect every output manually.

------------------------------------------------------------------------

# 50. Final Execution

The completed script is executed with:

``` powershell
& "c:\Data Analytics\Automated Commercial Performance Reporting System\.venv\Scripts\python.exe" "c:/Data Analytics/Automated Commercial Performance Reporting System/src/generate_adventureworks_report.py"
```

Successful execution produced:

``` text
============================================================
AUTOMATED COMMERCIAL PERFORMANCE REPORT
============================================================
Database engine created successfully.
Database: AdventureWorks2022
Report: reports\adventureworks_commercial_performance_report.xlsx
Sales detail extracted: 121317 rows
Commercial data extracted: 121317 rows
Commercial columns: 22

FINANCIAL VALIDATION
----------------------------------------
Revenue: 109846381.39988798
Cost: 97288600.8008
Gross Profit: 12557780.599088002
Gross Profit reconciliation difference: 1.862645149230957e-08
Fallback cost rows: 64
Unresolved cost rows: 0
Financial validation: PASS

Historical cost records: 121317
Reporting dataset: 121317 rows
Reporting columns: 28

Detail worksheets formatted successfully.
Executive trend chart added.

Excel workbook created.
Worksheets:
[
    'Executive Summary',
    'Monthly Performance',
    'Category Performance',
    'Product Performance',
    'Customer Performance',
    'Seller Performance'
]

Excel report saved successfully.

============================================================
FINAL WORKBOOK VALIDATION
============================================================
Worksheet structure: PASS
Executive Summary: PASS
Monthly Gross Margin format: 0.00%
Monthly Performance: PASS
Category Performance: PASS
Product Performance: PASS
Customer Performance: PASS
Seller Performance: PASS
Executive trend chart: PASS

FINAL WORKBOOK VALIDATION: PASS
```

------------------------------------------------------------------------

# 51. Development Issues and Resolutions

## 51.1 Historical cost mismatch

### Problem

The initial cost-date rule excluded EndDate.

### Result

``` text
121,237 matched
80 missing
```

### Resolution

Changed:

``` sql
OrderDate < EndDate
```

to:

``` sql
OrderDate <= EndDate
```

while retaining open-ended records with:

``` sql
EndDate IS NULL
```

------------------------------------------------------------------------

## 51.2 Pandas Period and Excel

### Problem

openpyxl raised:

``` text
ValueError:
Cannot convert Period('2011-05', 'M') to Excel
```

### Resolution

``` python
monthly_report_df["OrderMonth"] = (
    monthly_report_df["OrderMonth"]
    .astype(str)
)
```

------------------------------------------------------------------------

## 51.3 Excel file lock

### Problem

Python raised a `PermissionError` while attempting to overwrite the
workbook.

### Cause

The Excel file was open.

### Resolution

Close the workbook in Excel and rerun the script.

------------------------------------------------------------------------

## 51.4 Gross Margin display

### Problem

Python stores:

``` text
11.4321
```

while Excel percentage formatting expects:

``` text
0.114321
```

### Resolution

Executive Summary:

``` python
executive_sheet["B8"] = (
    executive_kpis["gross_margin_pct"] / 100
)
```

Detail sheets:

``` python
cell.value = cell.value / 100
cell.number_format = "0.00%"
```

------------------------------------------------------------------------

## 51.5 Incorrect validation column

### Problem

The validator originally checked:

``` python
monthly_sheet["E4"]
```

assuming GrossMarginPct was column E.

### Actual layout

``` text
A OrderMonth
B Revenue
C Cost
D GrossProfit
E SalesLines
F GrossMarginPct
```

Therefore E4 correctly had:

``` text
#,##0
```

because it was SalesLines.

### Resolution

The validator was changed to locate the column by its header:

``` python
monthly_header_map = {
    cell.value: cell.column
    for cell in monthly_sheet[3]
    if cell.value is not None
}

gross_margin_column = monthly_header_map[
    "GrossMarginPct"
]
```

This is more robust than fixed-position validation.

------------------------------------------------------------------------

# 52. Important Business Findings Produced by the Dataset

The reporting pipeline produced several commercially relevant patterns.

## Overall

``` text
Revenue = $109.85M
Gross Profit = $12.56M
Gross Margin = 11.43%
```

## Category

Bikes dominate the commercial population:

``` text
Revenue ≈ $94.65M
```

Accessories have the highest category margin:

``` text
≈ 49.88%
```

## Seller

Some sellers generate high revenue with very low or negative gross
margin.

For example, the final seller dataset showed:

``` text
Linda Mitchell
Revenue ≈ $10.37M
Gross Margin ≈ 1.66%
```

while:

``` text
Lynn Tsoflias
Revenue ≈ $1.42M
Gross Margin ≈ -6.19%
```

This demonstrates why revenue-only performance reporting can be
misleading.

## Customer

The customer dataset also showed several high-revenue customers with
negative gross profit.

This supports the need to report:

``` text
Revenue
Cost
Gross Profit
Gross Margin
```

rather than revenue alone.

------------------------------------------------------------------------

# 53. Anomaly Investigation That Was Performed

One significant monthly anomaly was investigated:

``` text
April 2012
```

The month showed negative gross profit.

The investigation found that the result was concentrated in Bikes,
particularly Mountain-100 products, where historical costs combined with
significant discounts resulted in sales below cost.

The source cost history supported the calculation.

The investigation was intentionally stopped after the business
explanation was established.

A large anomaly-detection engine was not added because that would expand
the project beyond the agreed reporting-automation scope.

------------------------------------------------------------------------

# 54. Completed Reporting Workbook

The final workbook contains exactly six worksheets:

``` text
Executive Summary
Monthly Performance
Category Performance
Product Performance
Customer Performance
Seller Performance
```

The report provides:

-   executive KPIs;
-   trend reporting;
-   category profitability;
-   top-product performance;
-   top-customer performance;
-   salesperson performance.

------------------------------------------------------------------------

# 55. Reporting Automation Pattern

The reusable pattern established by AdventureWorks is:

``` text
1. Connect
2. Identify source
3. Extract
4. Validate source population
5. Apply business rules
6. Reconcile key financial calculations
7. Build reporting datasets
8. Generate workbook
9. Format workbook
10. Add limited decision-useful visualization
11. Save
12. Reopen
13. Validate saved artifact
```

This pattern is more important than any individual SQL query.

------------------------------------------------------------------------

# 56. Design Principles Established

## Principle 1 --- Correct grain before aggregation

Do not aggregate until the transaction grain is understood.

## Principle 2 --- Business rules must be explicit

Historical cost methodology is part of the reporting definition.

## Principle 3 --- Validation must be risk-based

Do not build dozens of tests simply because the database contains dozens
of relationships.

## Principle 4 --- Financial metrics require reconciliation

Gross profit must reconcile:

``` text
Revenue - Cost
```

## Principle 5 --- Separate calculation from presentation

Python/pandas creates the reporting data.

openpyxl presents the reporting data.

## Principle 6 --- Validate the actual artifact

The saved workbook must be reopened and checked.

## Principle 7 --- Do not overbuild

The goal is a trustworthy automated report, not an unnecessarily large
analytics platform.

------------------------------------------------------------------------

# 57. What Is Reusable for Maven CRM

The AdventureWorks pipeline establishes several reusable patterns.

## Reusable

-   SQLAlchemy connection pattern;
-   source extraction functions;
-   pandas transformation pattern;
-   risk-based validation approach;
-   business-calculation layer;
-   report-data package;
-   Excel writer;
-   formatting function;
-   saved-artifact validation;
-   orchestration structure.

## Not automatically reusable

The following must be redesigned for Maven CRM:

-   source tables;
-   source grain;
-   business keys;
-   pipeline/opportunity definitions;
-   stage definitions;
-   CRM-specific metrics;
-   date logic;
-   business questions.

The second source must be understood independently before integration.

------------------------------------------------------------------------

# 58. Do Not Merge Sources Yet

The correct sequence is:

``` text
AdventureWorks
      ↓
Complete + validated

Maven CRM
      ↓
Understand + validate + report

Only then:

AdventureWorks + Maven CRM
      ↓
Assess whether cross-source integration is meaningful
```

The sources should not be joined simply because both contain commercial
information.

A proper integration requires compatible:

-   grain;
-   entities;
-   time definitions;
-   business definitions;
-   identifiers;
-   ownership concepts.

------------------------------------------------------------------------

# 59. Current Status

## AdventureWorks Pipeline

**COMPLETED**

The following have passed:

``` text
Database connection              PASS
Commercial extraction            PASS
Historical cost methodology      PASS
Cost fallback control            PASS
Financial reconciliation         PASS
Reporting dataset construction   PASS
Excel generation                 PASS
Worksheet formatting             PASS
Executive chart                  PASS
Saved workbook validation        PASS
```

------------------------------------------------------------------------

# 60. Next Phase

The next phase is **AdventureWorks Report Review**.

The review should inspect the actual Excel deliverable as a business
report:

1.  Executive Summary usability.
2.  KPI presentation.
3.  Trend chart readability.
4.  Monthly performance layout.
5.  Category performance readability.
6.  Product/customer/seller tables.
7.  Number formatting.
8.  Filters and frozen headers.
9.  Whether the report is decision-useful.
10. Any defects worth correcting.

Only after that review should development move to:

> **Maven CRM reporting pipeline.**

------------------------------------------------------------------------

# 61. Final Reference: End-to-End Logic

The complete AdventureWorks process can be summarized as:

``` text
AdventureWorks2022
        │
        ├── SalesOrderHeader
        ├── SalesOrderDetail
        ├── Customer
        ├── Person
        ├── SalesPerson
        ├── SalesTerritory
        ├── Product
        ├── ProductSubcategory
        ├── ProductCategory
        └── ProductCostHistory
                │
                ▼
        SQLAlchemy / pandas
                │
                ▼
        121,317 sales lines
                │
                ▼
        Historical cost matching
                │
                ├── 121,253 historical matches
                └── 64 controlled fallbacks
                │
                ▼
        ReportingUnitCost
                │
                ▼
        Revenue
        Cost
        Gross Profit
        Gross Margin
                │
                ▼
        Financial reconciliation
                │
                ▼
        Report datasets
                │
        ┌───────┼────────┬────────┬────────┐
        ▼       ▼        ▼        ▼        ▼
    Monthly Category Product Customer Seller
        │       │        │        │        │
        └───────┴────────┴────────┴────────┘
                        │
                        ▼
                 Excel workbook
                        │
                        ▼
              Presentation formatting
                        │
                        ▼
               Executive trend chart
                        │
                        ▼
                 Save workbook
                        │
                        ▼
              Reopen saved workbook
                        │
                        ▼
             FINAL VALIDATION: PASS
```

------------------------------------------------------------------------

# 62. Completion Statement

The AdventureWorks implementation is the first completed automated
reporting source in the Automated Commercial Performance Reporting
System.

It demonstrates a complete path from transactional source data to a
validated management report while maintaining explicit business logic,
financial controls, reusable Python components, and a clear separation
between data processing and presentation.

The implementation should now be treated as the **reference pattern**
for the Maven CRM phase---not as a template to copy blindly, but as the
architectural and engineering standard that the next source should meet.

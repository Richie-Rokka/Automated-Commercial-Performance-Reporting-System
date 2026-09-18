# src/adventureworks/extract.py

import pandas as pd


def extract_sales_detail(engine):
    """
    Extract the AdventureWorks sales transaction grain.

    Grain:
        One row per SalesOrderDetailID.
    """

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


def extract_commercial_data(engine):
    """
    Extract sales transactions with commercial dimensions.

    Grain:
        One row per SalesOrderDetailID.
    """

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


def extract_historical_costs(engine):
    """
    Extract historical product costs from AdventureWorks.

    The cost is matched to the sales order date using
    the effective historical cost period.
    """

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


def extract_current_product_costs(engine):
    """
    Extract current standard cost for each product.

    Used only when no applicable historical
    cost record exists.
    """

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
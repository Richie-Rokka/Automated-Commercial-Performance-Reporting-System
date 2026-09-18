# src/adventureworks/connection.py

from urllib.parse import quote_plus

from sqlalchemy import create_engine


SERVER = r"localhost\SQLEXPRESS"
DATABASE = "AdventureWorks2022"


def create_database_engine():
    """
    Create and return a SQLAlchemy engine
    for the AdventureWorks database.
    """

    connection_string = quote_plus(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={connection_string}"
    )

    return engine
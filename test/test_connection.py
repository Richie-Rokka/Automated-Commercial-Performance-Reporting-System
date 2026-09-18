from src.adventureworks.connection import create_database_engine
from sqlalchemy import text

engine = create_database_engine()

with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT
                @@SERVERNAME AS ServerName,
                DB_NAME() AS DatabaseName;
        """)
    )

    row = result.fetchone()

print("Server:", row.ServerName)
print("Database:", row.DatabaseName)
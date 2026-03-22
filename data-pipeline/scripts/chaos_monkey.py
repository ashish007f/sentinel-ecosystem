import duckdb
from loguru import logger
import sys
import os
import random

# Ensure src is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.config import settings

class ChaosMonkey:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(settings.DATABASE_PATH)
        self.conn = duckdb.connect(self.db_path)

    def inject_nulls(self, table: str = "silver_users", column: str = "user_id", percentage: float = 0.1):
        """Nullifies a percentage of values in a column."""
        logger.warning(f"Injecting NULLs into {table}.{column} ({percentage*100}%)...")
        # DuckDB doesn't support easy UPDATE with random in same way as Postgres, 
        # so we use a subquery or a temporary table
        query = f"""
        UPDATE {table} SET {column} = NULL 
        WHERE user_id IN (SELECT user_id FROM {table} ORDER BY random() LIMIT (SELECT CAST(COUNT(*)*{percentage} AS INT) FROM {table}));
        """
        self.conn.execute(query)
        logger.success(f"NULL injection complete for {table}.{column}")

    def delete_records(self, table: str = "silver_users", percentage: float = 0.2):
        """Deletes a percentage of records."""
        logger.warning(f"Deleting {percentage*100}% of records from {table}...")
        query = f"""
        DELETE FROM {table} 
        WHERE user_id IN (SELECT user_id FROM {table} ORDER BY random() LIMIT (SELECT CAST(COUNT(*)*{percentage} AS INT) FROM {table}));
        """
        self.conn.execute(query)
        logger.success(f"Deletions complete for {table}")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    monkey = ChaosMonkey()
    # Randomly pick a fault
    fault = random.choice(["nulls", "deletions"])
    if fault == "nulls":
        monkey.inject_nulls()
    else:
        monkey.delete_records()
    monkey.close()

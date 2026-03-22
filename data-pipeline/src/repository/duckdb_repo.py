import duckdb
from typing import Any, List, Optional, Tuple
from loguru import logger
from .base import AbstractRepository

class DuckDBRepository(AbstractRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = duckdb.connect(self.db_path)
        logger.info(f"Connected to DuckDB at {db_path}")

    def load_csv(self, csv_file: str, table_name: str) -> int:
        """Loads a CSV into DuckDB using read_csv_auto."""
        try:
            # Idempotent creation: create empty table with CSV schema if not exists
            self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM read_csv_auto('{csv_file}') LIMIT 0")
            # Insert data
            self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM read_csv_auto('{csv_file}')")
            return self.get_count(table_name)
        except Exception as e:
            logger.error(f"DuckDB Load Error: {e}")
            raise

    def run_transformation(self, query_name: str, target_table: str, source_table: str) -> int:
        """Centralized SQL for transformations."""
        if query_name == "silver_cleansing":
            query = f"""
            CREATE OR REPLACE TABLE {target_table} AS
            SELECT DISTINCT
                user_id,
                name,
                email,
                CAST(signup_date AS TIMESTAMP) as signup_timestamp,
                country,
                age,
                is_active
            FROM {source_table}
            WHERE user_id IS NOT NULL;
            """
        elif query_name == "gold_metrics":
            query = f"""
            CREATE OR REPLACE TABLE {target_table} AS
            SELECT 
                country,
                COUNT(user_id) as total_users,
                AVG(age) as avg_age,
                COUNT(CASE WHEN is_active THEN 1 END) as active_users
            FROM {source_table}
            GROUP BY country;
            """
        else:
            raise ValueError(f"Unknown transformation: {query_name}")

        self.conn.execute(query)
        return self.get_count(target_table)

    def get_count(self, table_name: str, filter_condition: Optional[str] = None) -> int:
        query = f"SELECT COUNT(*) FROM {table_name}"
        if filter_condition:
            query += f" WHERE {filter_condition}"
        return self.conn.execute(query).fetchone()[0]

    def get_distinct_count(self, table_name: str, column_name: str, filter_condition: Optional[str] = None) -> int:
        query = f"SELECT COUNT(DISTINCT {column_name}) FROM {table_name}"
        if filter_condition:
            query += f" WHERE {filter_condition}"
        return self.conn.execute(query).fetchone()[0]

    def get_metrics(self, table_name: str) -> List[Tuple[Any, ...]]:
        return self.conn.execute(f"SELECT * FROM {table_name}").fetchall()

    def inject_nulls(self, table_name: str, column_name: str, percentage: float):
        """Nullifies a percentage of values using DuckDB RANDOM()."""
        query = f"""
        UPDATE {table_name} SET {column_name} = NULL 
        WHERE user_id IN (
            SELECT user_id FROM {table_name} 
            ORDER BY random() 
            LIMIT (SELECT CAST(COUNT(*)*{percentage} AS INT) FROM {table_name})
        );
        """
        self.conn.execute(query)

    def delete_records(self, table_name: str, percentage: float):
        """Deletes a percentage of records using DuckDB RANDOM()."""
        query = f"""
        DELETE FROM {table_name} 
        WHERE user_id IN (
            SELECT user_id FROM {table_name} 
            ORDER BY random() 
            LIMIT (SELECT CAST(COUNT(*)*{percentage} AS INT) FROM {table_name})
        );
        """
        self.conn.execute(query)

    def close(self):
        self.conn.close()
        logger.info("DuckDB connection closed.")

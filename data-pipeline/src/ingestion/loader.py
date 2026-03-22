import duckdb
from loguru import logger
from ..config import settings
from pathlib import Path

class DuckDBLoader:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(settings.DATABASE_PATH)
        self.conn = duckdb.connect(self.db_path)

    def load_csv_to_bronze(self, csv_file: str, table_name: str = "bronze_users"):
        """Loads a CSV file into a DuckDB table."""
        logger.info(f"Loading {csv_file} into {table_name}...")
        try:
            # Check if table exists, if not create it using the CSV schema but with 0 rows
            self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM read_csv_auto('{csv_file}') LIMIT 0")
            
            # Now insert the actual data
            self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM read_csv_auto('{csv_file}')")
            
            count = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            logger.success(f"Total records in {table_name}: {count}")
        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            raise

    def close(self):
        self.conn.close()

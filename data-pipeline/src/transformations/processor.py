import duckdb
from loguru import logger
from ..config import settings

class SilverGoldProcessor:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(settings.DATABASE_PATH)
        self.conn = duckdb.connect(self.db_path)

    def process_silver(self, source_table: str = "bronze_users", target_table: str = "silver_users"):
        """Cleanses data: casts types, deduplicates, and filters active users."""
        logger.info(f"Transforming {source_table} to {target_table} (Silver Layer)...")
        
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
        self.conn.execute(query)
        count = self.conn.execute(f"SELECT COUNT(*) FROM {target_table}").fetchone()[0]
        logger.success(f"Silver layer complete. Count: {count}")

    def process_gold_active_users_by_country(self, source_table: str = "silver_users", target_table: str = "gold_user_metrics"):
        """Aggregates active users by country."""
        logger.info(f"Aggregating {source_table} to {target_table} (Gold Layer)...")
        
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
        self.conn.execute(query)
        count = self.conn.execute(f"SELECT COUNT(*) FROM {target_table}").fetchone()[0]
        logger.success(f"Gold layer complete. Total countries: {count}")

    def close(self):
        self.conn.close()

from loguru import logger
from ..repository.base import AbstractRepository

class SilverGoldProcessor:
    def __init__(self, repository: AbstractRepository):
        self.repo = repository

    def process_silver(self, source_table: str = "bronze_users", target_table: str = "silver_users"):
        """Cleanses data using the repository's silver transformation logic."""
        logger.info(f"Transforming {source_table} to {target_table} (Silver Layer)...")
        count = self.repo.run_transformation("silver_cleansing", target_table, source_table)
        logger.success(f"Silver layer complete. Count: {count}")

    def process_gold_active_users_by_country(self, source_table: str = "silver_users", target_table: str = "gold_user_metrics"):
        """Aggregates metrics using the repository's gold transformation logic."""
        logger.info(f"Aggregating {source_table} to {target_table} (Gold Layer)...")
        count = self.repo.run_transformation("gold_metrics", target_table, source_table)
        logger.success(f"Gold layer complete. Total countries: {count}")

    def close(self):
        pass

from loguru import logger
from ..repository.base import AbstractRepository

class DuckDBLoader:
    def __init__(self, repository: AbstractRepository):
        self.repo = repository

    def load_csv_to_bronze(self, csv_file: str, table_name: str = "bronze_users"):
        """Loads a CSV file into a table using the repository."""
        logger.info(f"Loading {csv_file} into {table_name}...")
        try:
            count = self.repo.load_csv(csv_file, table_name)
            logger.success(f"Total records in {table_name}: {count}")
        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            raise

    def close(self):
        # The repository is usually managed by the orchestrator, 
        # but we keep this for backwards compatibility if needed.
        pass

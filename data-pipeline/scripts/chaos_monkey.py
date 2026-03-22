from src.repository.duckdb_repo import DuckDBRepository
from src.config import settings
from loguru import logger
import sys
import os
import random

# Ensure src is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class ChaosMonkey:
    def __init__(self, repository: DuckDBRepository):
        self.repo = repository

    def run_fault(self, fault_type: str):
        if fault_type == "nulls":
            logger.warning("Injecting NULLs into bronze_users.user_id (10%)...")
            self.repo.inject_nulls("bronze_users", "user_id", 0.1)
            logger.success("NULL injection complete.")
        elif fault_type == "deletions":
            logger.warning("Deleting 20% of records from bronze_users...")
            self.repo.delete_records("bronze_users", 0.2)
            logger.success("Deletions complete.")

def main():
    repo = DuckDBRepository(str(settings.DATABASE_PATH))
    monkey = ChaosMonkey(repo)
    
    fault = random.choice(["nulls", "deletions"])
    try:
        monkey.run_fault(fault)
    finally:
        repo.close()

if __name__ == "__main__":
    main()

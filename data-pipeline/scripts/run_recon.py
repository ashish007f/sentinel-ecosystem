from src.reconciliation.reconciler import DataReconciler
from src.repository.duckdb_repo import DuckDBRepository
from src.config import settings
from loguru import logger
import sys
import os

# Ensure src is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    logger.add("logs/recon.log", rotation="1 MB")
    logger.info("Starting Reconciliation Job (Refactored)...")

    # Instantiate Repository
    repo = DuckDBRepository(str(settings.DATABASE_PATH))

    try:
        reconciler = DataReconciler(repository=repo)
        reconciler.run_reconciliation_report()
        logger.success("Reconciliation job completed.")

    except Exception as e:
        logger.error(f"Reconciliation job failed: {e}")
        sys.exit(1)
    finally:
        repo.close()

if __name__ == "__main__":
    main()

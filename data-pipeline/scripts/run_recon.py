from src.reconciliation.reconciler import DataReconciler
from loguru import logger
import sys
import os

# Ensure src is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    logger.add("logs/recon.log", rotation="1 MB")
    logger.info("Starting Reconciliation Job...")

    try:
        reconciler = DataReconciler()
        reconciler.run_reconciliation_report()
        reconciler.close()
        logger.success("Reconciliation job completed.")

    except Exception as e:
        logger.error(f"Reconciliation job failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

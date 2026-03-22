import pandas as pd
from loguru import logger
from ..config import settings
from ..repository.base import AbstractRepository

class DataReconciler:
    def __init__(self, repository: AbstractRepository):
        self.repo = repository

    def run_reconciliation_report(self):
        """Perform a full multi-layer reconciliation using the repository."""
        logger.info("Starting Multi-Layer Data Reconciliation Job...")
        report = {}

        # 1. Source (CSV) -> Bronze
        source_csvs = list(settings.DATA_DIR.glob("users_*.csv"))
        if not source_csvs:
            logger.warning("No source CSV files found for reconciliation.")
            report["source_to_bronze"] = "NO_DATA"
        else:
            total_source = sum(len(pd.read_csv(f)) for f in source_csvs)
            bronze_count = self.repo.get_count("bronze_users")
            report["source_count"] = total_source
            report["bronze_count"] = bronze_count
            report["source_to_bronze_diff"] = total_source - bronze_count

        # 2. Bronze -> Silver (Applying Business Rules)
        silver_count = self.repo.get_count("silver_users")
        
        # Expected Silver = Distinct(Bronze) where user_id is not null
        expected_silver = self.repo.get_distinct_count("bronze_users", "user_id", filter_condition="user_id IS NOT NULL")

        report["silver_count"] = silver_count
        report["expected_silver"] = expected_silver
        report["silver_unexplained_loss"] = expected_silver - silver_count

        # 3. Silver -> Gold (Aggregation Check)
        unique_countries_silver = self.repo.get_distinct_count("silver_users", "country")
        gold_country_count = self.repo.get_count("gold_user_metrics")
        
        report["gold_countries"] = gold_country_count
        report["expected_gold_countries"] = unique_countries_silver
        report["gold_integrity_check"] = "PASS" if gold_country_count == unique_countries_silver else "FAIL"

        self._log_report(report)
        return report

    def _log_report(self, report):
        logger.info("-" * 40)
        logger.info("   RECONCILIATION SUMMARY   ")
        logger.info("-" * 40)
        for key, val in report.items():
            logger.info(f"{key:25}: {val}")
        
        if report.get("silver_unexplained_loss", 0) > 0:
            logger.error(f"ALERT: Unexplained data loss of {report['silver_unexplained_loss']} records in Silver layer!")
        elif report.get("gold_integrity_check") == "FAIL":
            logger.error("ALERT: Gold layer aggregation mismatch!")
        else:
            logger.success("All layers are internally consistent.")
        logger.info("-" * 40)

    def close(self):
        pass

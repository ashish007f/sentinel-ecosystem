import duckdb
import pandas as pd
from loguru import logger
from ..config import settings
from pathlib import Path
import glob

class DataReconciler:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(settings.DATABASE_PATH)
        self.conn = duckdb.connect(self.db_path)

    def run_reconciliation_report(self):
        """Perform a full multi-layer reconciliation and return a summary report."""
        logger.info("Starting Multi-Layer Data Reconciliation Job...")
        report = {}

        # 1. Source (CSV) -> Bronze
        source_csvs = list(settings.DATA_DIR.glob("users_*.csv"))
        if not source_csvs:
            logger.warning("No source CSV files found for reconciliation.")
            report["source_to_bronze"] = "NO_DATA"
        else:
            # Sum total records in all CSVs (source of truth)
            total_source = sum(len(pd.read_csv(f)) for f in source_csvs)
            bronze_count = self.conn.execute("SELECT COUNT(*) FROM bronze_users").fetchone()[0]
            
            # Since my loader *appends* to bronze in my script (or recreates), 
            # we need to be careful. Let's assume bronze should be 1:1 with source.
            report["source_count"] = total_source
            report["bronze_count"] = bronze_count
            report["source_to_bronze_diff"] = total_source - bronze_count

        # 2. Bronze -> Silver (Applying Business Rules)
        # Rule 1: Silver drops NULL user_ids.
        # Rule 2: Silver deduplicates.
        bronze_metrics = self.conn.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(DISTINCT user_id) as distinct_ids,
                COUNT(*) FILTER (WHERE user_id IS NULL) as null_ids
            FROM bronze_users
        """).fetchone()
        
        silver_count = self.conn.execute("SELECT COUNT(*) FROM silver_users").fetchone()[0]
        
        # Better: Silver should match Bronze WHERE user_id IS NOT NULL AND DISTINCT
        expected_silver_query = "SELECT COUNT(DISTINCT user_id) FROM bronze_users WHERE user_id IS NOT NULL"
        expected_silver = self.conn.execute(expected_silver_query).fetchone()[0]

        report["silver_count"] = silver_count
        report["expected_silver"] = expected_silver
        report["silver_unexplained_loss"] = expected_silver - silver_count

        # 3. Silver -> Gold (Aggregation Check)
        # Rule: Gold should have a row for every country in Silver.
        unique_countries_silver = self.conn.execute("SELECT COUNT(DISTINCT country) FROM silver_users").fetchone()[0]
        gold_country_count = self.conn.execute("SELECT COUNT(*) FROM gold_user_metrics").fetchone()[0]
        
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
        self.conn.close()

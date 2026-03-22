# Sentinel Pipeline: Business Design & Logic Reference

This document defines the expected behavior of the data pipeline layers. Use this to verify if a discrepancy is an intended design or a bug.

## 1. Ingestion Layer (Source -> Bronze)
- **Objective:** Mirror Source CSVs into DuckDB with idempotency.
- **Expected Behavior:** `bronze_users` should have exactly the same number of rows as the unique records in the source CSVs.
- **Deduplication:** The pipeline does not currently perform upserts to bronze_users; it appends.

## 2. Cleansing Layer (Bronze -> Silver)
- **Objective:** Produce a clean, typed, and unique dataset.
- **Logic Rules:**
    - `CAST(signup_date AS TIMESTAMP)`: Converts ISO strings.
    - `DISTINCT`: Removes identical row duplicates.
    - `WHERE user_id IS NOT NULL`: Drops any record missing a primary identifier.
- **Acceptable Data Loss:** If Bronze contains NULLs or duplicate rows, Silver *must* have a lower count.

## 3. Metric Layer (Silver -> Gold)
- **Objective:** Aggregate metrics by country.
- **Logic:** `GROUP BY country`.
- **Integrity Constraint:** The row count of `gold_user_metrics` must exactly match `SELECT COUNT(DISTINCT country) FROM silver_users`.

## 4. Reconciliation Job (The Truth)
- **Logic:** `Unexplained Loss = (Bronze Count - NULL Count) - Silver Count`.
- **Verdict:** 
    - If `Unexplained Loss == 0`: SUCCESS.
    - If `Unexplained Loss > 0`: BUG (Records are being dropped incorrectly) or records are being manipulated manually

# Sentinel Data Pipeline

A robust ELT (Extract, Load, Transform) pipeline designed for observability and fault-tolerance testing.

## 🏗️ Architecture

-   **Ingestion:** Mock user data generated via `Faker` and loaded into DuckDB `bronze_users`.
-   **Transformation:** 
    -   **Silver Layer:** Deduplicated and typed data with NULL filtering (`silver_users`).
    -   **Gold Layer:** Aggregated metrics by country (`gold_user_metrics`).
-   **Reconciliation:** An internal audit job that compares cource vs. Bronze vs. Silver vs. Gold to find unexplained data loss.

## 🏃 Running the Pipeline

Ensure you are in the `data-pipeline/` directory.

### 1. Execute E2E Pipeline
Generates fresh data and runs all transformations.
```bash
uv run scripts/run_pipeline.py
```

### 2. Run Integrity Audit (Reconciliation)
Compares all layers and logs a summary report to `logs/recon.log`.
```bash
uv run scripts/run_recon.py
```

### 3. Fault Injection (Chaos Monkey)
Simulates real-world data corruption by deleting records or injecting NULLs.
```bash
uv run scripts/chaos_monkey.py
```

## 📊 Data Inspection
You can explore the DuckDB warehouse using the provided Jupyter Notebook: `duckdb_notebook.ipynb`.

## 📁 Key Files
- `src/ingestion/loader.py`: Ingestion logic.
- `src/transformations/processor.py`: Silver/Gold transformation logic.
- `src/reconciliation/reconciler.py`: Business logic for the audit.

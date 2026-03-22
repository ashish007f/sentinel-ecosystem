# Project Objective: Data Medallion Pipeline (Target)
Build a local-first data pipeline that simulates a production environment for testing reconciliation and RCA.

## Tech Stack
- Database: DuckDB (Local-first, BigQuery compatible SQL).
- Language: Python 3.11+.
- Libraries: pandas, duckdb, faker (for data gen).

## Step-by-Step Implementation
1. **Infrastructure Setup**:
   - Create a `data/` directory to host `product_data.db`.
   - Initialize a SQLAlchemy-compatible connection string for DuckDB.

2. **Data Generation (The Service Layer)**:
   - Create `mock_orders.py`: Generate synthetic JSON order events (ID, timestamp, customer_id, amount, status).
   - Simulate a "Kafka Topic" by appending these events to a local `stream_buffer.csv`.

3. **Medallion Layers**:
   - **Bronze**: Load raw CSV data into a DuckDB table `bronze_orders` with no transformations.
   - **Silver**: Create a view/table `silver_orders` that casts types, handles nulls, and deduplicates.
   - **Gold**: Create `gold_daily_revenue` as an aggregation of `silver_orders` by day.

4. **The "Chaos Monkey" (Testing Tool)**:
   - Create `inject_fault.py`: A script that manually deletes records from Silver or nulls out values in Bronze to create "Data Gaps" for the Agent to find.

## Deliverables
- A script `run_pipeline.py` that executes the full E2E flow.
- A README explaining the schema.

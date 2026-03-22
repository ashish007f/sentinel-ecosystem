import duckdb
from loguru import logger
from config import settings

def query_db(query: str) -> str:
    """
    Executes a SQL query against the Sentinel Warehouse (DuckDB).
    Use this to inspect tables (bronze_users, silver_users, gold_user_metrics).
    
    Args:
        query: The SQL query to execute.
    """
    db_path = str(settings.DB_PATH)
    logger.info(f"Agent executing SQL: {query}")
    try:
        conn = duckdb.connect(db_path, read_only=True)
        result = conn.execute(query).fetch_df().head(20).to_string()
        conn.close()
        return result
    except Exception as e:
        logger.error(f"SQL Error: {e}")
        return f"Error executing query: {str(e)}"

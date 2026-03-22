from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

class AbstractRepository(ABC):
    """
    Abstract interface for data warehouse operations.
    Implementing this class allows switching between different warehouses 
    (DuckDB, Postgres, Snowflake, etc.) without changing business logic.
    """

    @abstractmethod
    def load_csv(self, csv_file: str, table_name: str) -> int:
        """Loads a CSV file into a table and returns the total row count."""
        pass

    @abstractmethod
    def run_transformation(self, query_name: str, target_table: str, source_table: str) -> int:
        """Executes a named transformation and returns the row count of the target table."""
        pass

    @abstractmethod
    def get_count(self, table_name: str, filter_condition: Optional[str] = None) -> int:
        """Returns the row count of a table, optionally with a filter."""
        pass

    @abstractmethod
    def get_distinct_count(self, table_name: str, column_name: str, filter_condition: Optional[str] = None) -> int:
        """Returns the distinct count of a column."""
        pass

    @abstractmethod
    def get_metrics(self, table_name: str) -> List[Tuple[Any, ...]]:
        """Generic method to fetch results for reporting."""
        pass

    @abstractmethod
    def inject_nulls(self, table_name: str, column_name: str, percentage: float):
        """Nullifies a percentage of values in a column for testing."""
        pass

    @abstractmethod
    def delete_records(self, table_name: str, percentage: float):
        """Deletes a percentage of records for testing."""
        pass

    @abstractmethod
    def close(self):
        """Closes the connection."""
        pass

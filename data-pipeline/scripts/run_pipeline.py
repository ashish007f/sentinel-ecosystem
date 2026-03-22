from src.services.producer import MockProducer
from src.ingestion.loader import DuckDBLoader
from src.transformations.processor import SilverGoldProcessor
from src.repository.duckdb_repo import DuckDBRepository
from src.config import settings
from loguru import logger
import sys
import os

# Ensure src is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    logger.add("logs/pipeline.log", rotation="10 MB")
    logger.info("Starting Data Pipeline E2E (Refactored)...")

    # Instantiate Repository
    repo = DuckDBRepository(str(settings.DATABASE_PATH))

    try:
        # Step 1: Mock Data Production
        producer = MockProducer(records=200)
        csv_file = producer.generate_users()

        # Step 2: Bronze Ingestion
        loader = DuckDBLoader(repository=repo)
        loader.load_csv_to_bronze(csv_file)

        # Step 3: Silver & Gold Transformations
        processor = SilverGoldProcessor(repository=repo)
        processor.process_silver()
        processor.process_gold_active_users_by_country()

        logger.success("Pipeline execution completed successfully.")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)
    finally:
        repo.close()

if __name__ == "__main__":
    main()

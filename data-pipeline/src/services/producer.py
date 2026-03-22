import pandas as pd
from faker import Faker
from loguru import logger
from datetime import datetime
import uuid
import random
from ..config import settings

class MockProducer:
    def __init__(self, records: int = 100):
        self.fake = Faker()
        self.records = records

    def generate_users(self, output_path: str = None) -> str:
        """Generates mock user registration data."""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = settings.DATA_DIR / f"users_{timestamp}.csv"

        logger.info(f"Generating {self.records} mock user records...")
        data = []
        for _ in range(self.records):
            data.append({
                "user_id": str(uuid.uuid4()),
                "name": self.fake.name(),
                "email": self.fake.email(),
                "signup_date": self.fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
                "country": self.fake.country(),
                "age": random.randint(18, 80),
                "is_active": random.choice([True, True, True, False])  # 25% inactive
            })

        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        logger.success(f"Successfully saved mock data to {output_path}")
        return str(output_path)

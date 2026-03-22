from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Project Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"

    # Database Settings
    DATABASE_NAME: str = "sentinel_warehouse.db"
    DATABASE_PATH: Optional[Path] = None

    def __init__(self, **values):
        super().__init__(**values)
        if not self.DATABASE_PATH:
            self.DATABASE_PATH = self.DATA_DIR / self.DATABASE_NAME
        
        # Ensure directories exist
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()

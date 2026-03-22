from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class AgentSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Paths to the Target (data-pipeline)
    PIPELINE_ROOT: Path = Path(__file__).parent.parent / "data-pipeline"
    DB_PATH: Path = PIPELINE_ROOT / "data" / "sentinel_warehouse.db"
    LOGS_PATH: Path = PIPELINE_ROOT / "logs" / "pipeline.log"
    RECON_LOGS_PATH: Path = PIPELINE_ROOT / "logs" / "recon.log"

    MODEL_NAME: str = model_config.get("OLLAMA_MODEL_NAME", "openai/qwen3.5")  # Default model, can be overridden by .env

settings = AgentSettings()

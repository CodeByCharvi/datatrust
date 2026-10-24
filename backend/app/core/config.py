from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    llm_api_key: str
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = ""

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


settings = Settings()
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

class ProjectSettings(BaseSettings):
    LANGFW_BASE_URL: str = os.environ.get("LANGFW_BASE_URL", "http://localhost")
    LANGFW_PORT: int = int(os.environ.get("LANGFW_PORT", "7860"))
    LANGFW_API_KEY: str | None = os.environ.get("LANGFW_API_KEY")
    LANGFW_FLOW_ID: str | None = os.environ.get("LANGFW_FLOW_ID")
    LANGFW_PROJECT_ID: str | None = os.environ.get("LANGFW_PROJECT_ID")

    APP_NAME: str = "Green Era Baru"

    model_config = SettingsConfigDict(env_file=str(env_path), extra="ignore")

    @field_validator("LANGFW_BASE_URL")
    @classmethod
    def _ensure_scheme(cls, v: str) -> str:
        # If only fill with domain in env
        if not v.startswith("http://") and not v.startswith("https://"):
            return "http://" + v
        return v

project_settings = ProjectSettings()

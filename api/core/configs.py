import os

from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

from pathlib import Path
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

class ProjectSettings(BaseSettings):
    LANGFW_BASE_URL: str = os.environ.get("LANGFW_BASE_URL", "localhost")
    LANGFW_PORT: str = os.environ.get("LANGFW_PORT", "7860")
    LANGFW_API_KEY: str | None = os.environ.get("LANGFW_API_KEY")
    LANGFW_PROJECT_ID: str | None = os.environ.get("LANGFW_PROJECT_ID")
    APP_NAME: str = "Green Era Baru"

    class Config:
        env_file = "../.env"


project_settings = ProjectSettings()
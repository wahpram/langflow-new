from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

class ProjectSettings(BaseSettings):
    LANGFLOW_BASE_URL: str = "http://localhost:7860" # Mungkin ganti ke AnyHTTPUrl
    LANGFLOW_API_KEY: str | None = None
    LANGFLOW_API_ID: str | None = None
    APP_NAME: str = "Green Era Baru"

    class Config:
        env_file = ".env"


project_settings = ProjectSettings()
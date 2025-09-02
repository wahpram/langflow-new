from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    LANGFLOW_BASE_URL: AnyHttpUrl = "http://localhost:7860"
    LANGFLOW_API_KEY: str | None = None
    LANGFLOW_API_ID: str
    APP_NAME: str = "Green Era Baru"

    class Config:
        env_file = ".env"


settings = Settings()
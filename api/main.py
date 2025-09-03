from fastapi import FastAPI
from api.core.configs import project_settings as settings
from api.routers import api_router

app = FastAPI(title=settings.APP_NAME)

# semua endpoint dikumpulkan di api_router
app.include_router(api_router)
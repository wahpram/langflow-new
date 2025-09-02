from fastapi import FastAPI
from core.configs import settings

app = FastAPI(title=settings.APP_NAME)

@app.get("/health")
async def health():
    return {"status": "ok"}


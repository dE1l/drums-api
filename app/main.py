from fastapi import FastAPI

from app.api.login import router as login_router
from app.api.profile import router as profile_router
from app.utils.logging import AppLogger

logger = AppLogger.__call__().get_logger()

app = FastAPI(title="Drums API", version="0.1")

app.include_router(login_router)
app.include_router(profile_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)

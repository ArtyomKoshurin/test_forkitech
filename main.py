from contextlib import asynccontextmanager

from fastapi import FastAPI

from tron.database import engine, Base
from routes.wallet import router as wallet_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(wallet_router)

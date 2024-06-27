from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from db.config import db
from api.main_routers import mainRouter
from api.models_init import Meals
from redis import asyncio as aioredis

from config import settings


async def startup():
    await init_beanie(
        database=db,
        document_models=[
            Meals,
        ]
    )
    app.include_router(mainRouter)
    redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}",
                              encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


async def shutdown():
    # Add any shutdown logic here, if needed
    pass


app = FastAPI(on_startup=[startup], on_shutdown=[shutdown], title="Сервис блюд")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

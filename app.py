from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from db.config import db
from api.main_routers import mainRouter
from api.models_init import Meals


async def startup():
    await init_beanie(
        database=db,
        document_models=[
            Meals,
        ]
    )


async def shutdown():
    # Add any shutdown logic here, if needed
    pass


app = FastAPI(on_startup=[startup], on_shutdown=[shutdown])

app.include_router(mainRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
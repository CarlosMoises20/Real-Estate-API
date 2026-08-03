from fastapi import FastAPI
from backend.app.routes.items import router as items_router
from backend.app.middleware.timer import timer_middleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.middleware("http")(timer_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)
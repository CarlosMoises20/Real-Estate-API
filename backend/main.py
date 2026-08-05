from fastapi import FastAPI
from backend.app.routes.items import router as items_router
from backend.app.middleware.timer import timer_middleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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

if __name__ == "__main__":
    
    # NOTE: to test on Swagger UI: http://localhost:8001/docs
    
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
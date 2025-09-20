from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ua.api import router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/ua", tags=["UA"])

if __name__ == "__main__":
    uvicorn.run(
        "ua.main:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )
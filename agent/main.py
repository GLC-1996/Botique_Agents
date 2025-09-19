# agent/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from agent.agent_api import router as agent_router

app = FastAPI(
    title="Agent Service",
    description="AI agents for generating promotional strategies",
    version="1.0.0"
)

# Add CORS middleware for demo purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include agent router
app.include_router(agent_router, prefix="/agent", tags=["Agent"])

@app.get("/")
def root():
    """Health check endpoint"""
    return {"message": "Agent Service is running", "status": "healthy"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "agent"}

if __name__ == "__main__":
    uvicorn.run(
        "agent.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )

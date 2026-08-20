"""
RoboPulse Fleet Command Center
Day 4 - FastAPI application entrypoint.

Run from backend/ with the venv active:
    fastapi dev app/main.py

Day 9 Answer Key - Phase B additions made    
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import robots, missions, auth

#set up the FastAPI application with a title, description, and version. 
# This metadata is used in the automatically generated OpenAPI documentation.
app = FastAPI(
    title="RoboPulse Fleet Command Center",
    description=(
        "Fleet management API for Apex Robotics' autonomous "
        "inspection rovers and aerial drones."
    ),
    version="0.2.0", #bumped from "0.1.0"
)

FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")
print(f"DEBUG FRONTEND_ORIGIN={FRONTEND_ORIGIN!r}")

app.add_middleware(
    CORSMiddleware,
    #note the endpoint here is from Vite's dev server for our frontend
allow_origins=[FRONTEND_ORIGIN],
    #this allows us to pass an Authorization header (JWT)
    allow_credentials=True,
    #allows all methods and all headers through
    allow_methods=["*"],
    allow_headers=["*"]
)

#include the /robots router in the FastAPI application. This means that all routes defined
# in the robots router will be available under the /robots path.
app.include_router(robots.router)
app.include_router(missions.router)
app.include_router(auth.router)

#A simple health check endpoint to verify that the API is running.
@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/version", tags=["health"])
async def version() -> dict[str, str]:
    return {"version": app.version}
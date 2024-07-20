"""
This file will serve as the entry point for
the application.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
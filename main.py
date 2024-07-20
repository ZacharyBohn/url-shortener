"""
This file will serve as the entry point for
the application.
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/list_urls")
async def list_urls():
  return {"message": "ok"}
  
@app.get("/redirect")
async def redirect(short_url: str):
  return {"message": "ok"}
  
@app.post("/shorten_url")
async def shorten_url(url: str, short_url: str | None):
  return {"message": "ok"}
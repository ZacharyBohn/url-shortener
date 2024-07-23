from fastapi import APIRouter

router = APIRouter()

@router.post("/list_urls")
async def shorten_url(url: str, short_url: str | None):
  return {"message": "ok"}
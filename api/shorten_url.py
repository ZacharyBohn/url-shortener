from fastapi import APIRouter

router = APIRouter()

@router.get("/shorten_url")
async def list_urls(url: str, short_url: str | None):
  return {"message": "ok"}
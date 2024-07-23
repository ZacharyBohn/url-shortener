from fastapi import APIRouter

router = APIRouter()

@router.post("/shorten_url")
async def shorten_url(url: str, short_url: str | None):
  return {"message": "ok"}
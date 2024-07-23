from fastapi import APIRouter

router = APIRouter()

@router.get("/shorten_url")
async def list_urls():
  return {"message": "ok"}
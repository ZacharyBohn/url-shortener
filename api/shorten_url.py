from fastapi import APIRouter

router = APIRouter()

@router.get("/list_urls")
async def list_urls():
  return {"message": "ok"}
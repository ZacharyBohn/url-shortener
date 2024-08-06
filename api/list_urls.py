from fastapi import APIRouter
from schemas.list_urls_response import ListUrlsResponse

router = APIRouter()

@router.post("/list_urls", response_model=ListUrlsResponse)
async def list_urls():
	return {"message": "ok"}
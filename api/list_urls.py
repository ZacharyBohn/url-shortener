from fastapi import APIRouter
from schemas.list_urls_response import ListUrlsResponse

router = APIRouter()

@router.post("/list_urls", response_model=ListUrlsResponse)
async def shorten_url(url: str, short_url: str | None):
	return {"message": "ok"}
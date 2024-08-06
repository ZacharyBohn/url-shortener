from fastapi import APIRouter

router = APIRouter()

@router.get("/redirect")
async def redirect(short_url: str):
	return {"message": "ok"}
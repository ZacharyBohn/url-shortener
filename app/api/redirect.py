from fastapi import APIRouter, Response

from app.dependency_injector.di import DI
from app.schemas.error_response import ErrorReponse
from app.schemas.redirect_response import RedirectResponse

router = APIRouter()

@router.get("/redirect")
async def redirect(
	response: Response,
	short_url: str,
	):
	redirect_service = DI.instance().redirect_service
	original_url = redirect_service.redirect(short_url=short_url)
	if original_url is None:
		response.status_code = 400
		return ErrorReponse(
			error="Short url given is not associated with any original urls"
			)
	return RedirectResponse(original_url=original_url)
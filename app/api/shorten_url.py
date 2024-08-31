from typing import Optional
from fastapi import APIRouter, Response

from app.interfaces.shorten_url_interface import IShortenUrl
from app.services.shorten_url_service import InvalidUrlException
from app.schemas.short_url_response import ShortUrlResponse
from app.schemas.error_response import ErrorReponse
from app.dependency_injector.di import DI

router = APIRouter()

@router.post("/shorten_url")
async def shorten_url(
	response: Response,
	url: str,
	short_url_id: Optional[str] = None,
	):
	shorten_url_service: IShortenUrl = DI.instance().shorten_url_service
	
	try:
		generated_short_url: str = shorten_url_service.shorten_url(
			url=url,
			custom_short_url_id=short_url_id,
		)
		return ShortUrlResponse(
			short_url=generated_short_url,
			original_url=url,
		)
	except InvalidUrlException:
		# 400 =
		# the client sent an incorrect request
		response.status_code = 400
		return ErrorReponse(error='Invalid custom URL')
	except Exception as e:
		print(e)
		# 500 =
		# internal server error
		response.status_code = 500
		return ErrorReponse(error='Internal server error')
		
	

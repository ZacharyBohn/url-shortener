from fastapi import APIRouter, Response

from ..interfaces.shorten_url import IShortenUrlService
from services.shorten_url_service import InvalidUrlException
from schemas.short_url_response import ShortUrlResponse
from schemas.error_response import ErrorReponse
from interfaces.di import DI

router = APIRouter()

@router.get("/shorten_url")
async def shorten_url(url: str, short_url: str | None, response: Response):
	shorten_url_service: IShortenUrlService = DI.instance().shorten_url_service
	
	if short_url == None:
		try:
			generated_short_url: str = shorten_url_service.shorten_url(
				url=url,
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
		except:
			# 500 =
			# internal server error
			response.status_code = 500
			return ErrorReponse(error='Internal server error')

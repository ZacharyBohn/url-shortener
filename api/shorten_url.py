from fastapi import APIRouter, Response

from service.shorten_url import InvalidUrlException, generate_short_url
from schemas.short_url_response import ShortUrlResponse
from schemas.error_response import ErrorReponse

router = APIRouter()

@router.get("/shorten_url")
async def list_urls(url: str, short_url: str | None, response: Response):
	if short_url == None:
		try:
			generated_short_url: str = generate_short_url(
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

from typing import Dict
from fastapi import APIRouter, Response

from schemas.error_response import ErrorReponse
from dependency_injector.di import DI
from schemas.list_urls_response import ListUrlsResponse

router = APIRouter()

@router.get("/list_urls")
def list_urls(response: Response):
	try:
		list_urls_service = DI.instance().list_urls_service
		short_urls: Dict[str, str] = list_urls_service.list_urls()
		return ListUrlsResponse(short_urls=short_urls)
	except Exception as e:
		print(e)
		response.status_code = 500
		return ErrorReponse(error="Internal server error")

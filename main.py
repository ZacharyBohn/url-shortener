from fastapi import FastAPI

from api import list_urls
from api import redirect
from api import shorten_url
from db.db import Db
from utils.utilities import Utilities
from services.shorten_url_service import ShortenUrlService
from services.redirect_service import RedirectService
from services.list_urls_service import ListUrlsService
from dependency_injector.di import DI

# TODO: fill in with the actual domain
domain: str = 'domain.com'
short_id_length: int = 6

def create_app() -> FastAPI:
	app = FastAPI()
	app.include_router(list_urls.router)
	app.include_router(redirect.router)
	app.include_router(shorten_url.router)

	@app.get('/ping')
	def ping(): # type: ignore
		return 'ok'
	return app

if __name__ == "__main__":
	DI(
		list_urls_service=ListUrlsService(),
		redirect_service=RedirectService(),
		shorten_url_service=ShortenUrlService(),
		utils=Utilities(),
		db=Db(),
	)
	app = create_app()
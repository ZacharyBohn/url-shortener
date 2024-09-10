from fastapi import FastAPI

from app.api import list_urls
from app.api import redirect
from app.api import shorten_url
from app.database.db import DB
from app.interfaces.logger_interface import LogLevel
from app.utils.utilities import Utilities
from app.services.shorten_url_service import ShortenUrlService
from app.services.redirect_service import RedirectService
from app.services.list_urls_service import ListUrlsService
from app.dependency_injector.di import DI
from app.utils.logger import Logger

def create_app() -> FastAPI:
	app = FastAPI()
	app.include_router(list_urls.router)
	app.include_router(redirect.router)
	app.include_router(shorten_url.router)

	@app.get("/ping")
	def ping(): # type: ignore
		return "ok"
	return app

DI(
	list_urls_service=ListUrlsService(),
	redirect_service=RedirectService(),
	shorten_url_service=ShortenUrlService(),
	utils=Utilities(),
	db=DB,
	logger=Logger(""),
)
DI.instance().logger.setLogLevel(LogLevel.INFO)
DI.instance().db.connect()
app = create_app()
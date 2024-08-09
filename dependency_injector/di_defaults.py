from db.db import Db
from utils.utilities import Utilities
from services.shorten_url_service import ShortenUrlService
from services.redirect import RedirectService
from services.list_urls import ListUrlsService
from di import DI


def set_di_production_defaults() -> DI:
	return DI(
		list_urls_service=ListUrlsService(),
		redirect_service=RedirectService(),
		shorten_url_service=ShortenUrlService(),
		utils=Utilities(),
		db=Db(),
	)
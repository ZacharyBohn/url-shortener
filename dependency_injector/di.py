from typing import Optional

from ..db.db import Db
from utils.utilities import Utilities

from services.redirect import RedirectService
from services.list_urls import ListUrlsService
from services.shorten_url_service import ShortenUrlService


# Dependency injector
#
# This class will assign production defaults
# if no services are provided
class DI:
	@staticmethod
	def instance() -> 'DI':
		if DI._instance is None:
			DI._instance = DI()
		return DI._instance

	_instance: 'DI | None'

	def __init__(
			self,
			list_urls_service: Optional[ListUrlsService] = None,
			redirect_service: Optional[RedirectService] = None,
			shorten_url_service: Optional[ShortenUrlService] = None,
			utils: Optional[Utilities] = None,
			db: Optional[Db] = None,
			) -> None:
		if DI._instance is not None:
			raise Exception('Singleton already initialized')
		
		self.list_urls_service: ListUrlsService = list_urls_service \
			or ListUrlsService()
		self.redirect_service: RedirectService = redirect_service \
			or RedirectService()
		self.shorten_url_service: ShortenUrlService = shorten_url_service \
			or ShortenUrlService()
		self.utils = utils or Utilities()
		self.db = db or Db()
		return
	
	@staticmethod
	def reset() -> None:
		DI._instance = None
		return
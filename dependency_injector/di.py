from typing import TYPE_CHECKING
from utils.utilities import Utilities

from services.redirect import RedirectService
from services.list_urls import ListUrlsService
from services.shorten_url_service import ShortenUrlService

if TYPE_CHECKING:
	from db.db import Db


# Dependency injector
#
# This class will assign production defaults
# if no services are provided
class DI:
	@staticmethod
	def instance() -> 'DI':
		if DI._instance is None:
			raise Exception("DI not initialized")
		return DI._instance

	_instance: 'DI | None'

	def __init__(
			self,
			list_urls_service: ListUrlsService,
			redirect_service: RedirectService,
			shorten_url_service: ShortenUrlService,
			utils: Utilities,
			db: Db,
			) -> None:
		if DI._instance is not None:
			raise Exception('Singleton already initialized')
		
		self.list_urls_service: ListUrlsService = list_urls_service
		self.redirect_service: RedirectService = redirect_service
		self.shorten_url_service: ShortenUrlService = shorten_url_service
		self.utils = utils
		self.db = db
		return
	
	@staticmethod
	def reset() -> None:
		"""
		This function should only be called by tests.
		"""
		DI._instance = None
		return
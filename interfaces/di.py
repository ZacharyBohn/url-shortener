from typing import Optional

from ..utils.utilities import Utilities

from .utilities import IUtilities
from ..services.redirect import RedirectService
from ..services.list_urls import ListUrlsService
from .redirect import IRedirectService
from .list_urls import IListUrlsService
from .shorten_url import IShortenUrlService
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
			list_urls_service: Optional[IListUrlsService] = None,
			redirect_service: Optional[IRedirectService] = None,
			shorten_url_service: Optional[IShortenUrlService] = None,
			utils: Optional[IUtilities] = None,
			) -> None:
		if DI._instance is not None:
			raise Exception('Singleton already initialized')
		
		self.list_urls_service: IListUrlsService = list_urls_service \
			or ListUrlsService()
		self.redirect_service: IRedirectService = redirect_service \
			or RedirectService()
		self.shorten_url_service: IShortenUrlService = shorten_url_service \
			or ShortenUrlService()
		self.utils = utils or Utilities()
		return
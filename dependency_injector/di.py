from interfaces.db_interface import IDB
from interfaces.utilities_interface import IUtilities
from interfaces.shorten_url_interface import IShortenUrl
from interfaces.redirect_interface import IRedirect
from interfaces.list_urls_interface import IListUrls


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
			list_urls_service: IListUrls,
			redirect_service: IRedirect,
			shorten_url_service: IShortenUrl,
			utils: IUtilities,
			db: IDB,
			) -> None:
		if DI._instance is not None:
			raise Exception('Singleton already initialized')
		
		self.list_urls_service: IListUrls = list_urls_service
		self.redirect_service: IRedirect = redirect_service
		self.shorten_url_service: IShortenUrl = shorten_url_service
		self.utils: IUtilities = utils
		self.db: IDB = db
		return
	
	@staticmethod
	def reset() -> None:
		"""
		This function should only be called by tests.
		"""
		DI._instance = None
		return
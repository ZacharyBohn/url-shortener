from abc import ABC, abstractmethod

from services.shorten_url_service import UrlScheme

class IShortenUrlService(ABC):
	@abstractmethod
	def shorten_url(
		self,
		url: str,
		custom_short_url: str | None = None,
		scheme: UrlScheme = UrlScheme.HTTPS,
		) -> str:
		pass
	
	@abstractmethod
	def _is_valid_url(self, url: str) -> bool:
		pass
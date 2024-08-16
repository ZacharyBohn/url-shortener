from abc import ABC, abstractmethod

from interfaces.url_schemes import UrlScheme

class IShortenUrl(ABC):
	@abstractmethod
	async def shorten_url(
		self,
		url: str,
		custom_short_url_id: str | None = None,
		scheme: UrlScheme = UrlScheme.HTTPS,
		) -> str:
		pass
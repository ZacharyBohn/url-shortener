from dependency_injector.di import DI

from exceptions.exceptions import InvalidUrlException
from interfaces.shorten_url_interface import IShortenUrl
from interfaces.url_schemes import UrlScheme
from main import domain, short_id_length
from utils.utilities import Utilities


class ShortenUrlService(IShortenUrl):
	async def shorten_url(
		self,
		url: str,
		custom_short_url_id: str | None = None,
		scheme: UrlScheme = UrlScheme.HTTPS,
		) -> str:
		"""Generates a short url given a real url
		
		Args:
			url: the real URL that a short url will be generated for
			short_id_length: how long the short url id will be
			scheme: used to specify either http or https
			domain_name: the domain name of this service. This is be
				the domain name of the generated short url
		
		Returns:
			A short url generated using the given url
		
		Raises:
			InvalidUrlException: if the given url is not in a valid format
		"""
		utils: Utilities = DI.instance().utils
		if not utils.is_valid_url(url):
			raise InvalidUrlException("The provided URL was not valid.")
		random_sequence: str
		if custom_short_url_id:
			random_sequence = await DI.instance().db.create_short_url(url, custom_short_url_id)
		else:
			random_sequence = DI.instance().utils.generate_random_string(short_id_length)
			random_sequence = await DI.instance().db.create_short_url(url)
		short_url: str = f"{scheme.value}://{domain}/{random_sequence}"
		return short_url
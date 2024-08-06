import re
from enum import Enum

from dependency_injector.di import DI

from main import domain, short_id_length

class InvalidUrlException(Exception): pass

class UrlScheme(Enum):
	HTTP = "http"
	HTTPS = "https"
	FTP = "ftp"
	MAILTO = "mailto"
	FILE = "file"
	TEL = "tel"
	NEWS = "news"
	IRC = "irc"
	RTSP = "rtsp"
	SPOTIFY = "spotify"
	SFTP = "sftp"
	SSH = "ssh"
	GIT = "git"
	SVN = "svn"
	MAGNET = "magnet"
	ED2K = "ed2k"
	AFP = "afp"
	NFS = "nfs"
	LDAP = "ldap"
	BITCOIN = "bitcoin"

class ShortenUrlService:
	def shorten_url(
		self,
		url: str,
		custom_short_url: str | None = None,
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
		if not self._is_valid_url(url):
			raise InvalidUrlException("The provided URL was not valid.")
		random_sequence: str = DI.instance().utils.generate_random_string(short_id_length)
		short_url: str = f"{scheme.value}://{domain}/{random_sequence}"
		
		# TODO: add short url pair to db
		
		return short_url

	def _is_valid_url(self, url: str) -> bool:
		valid_url_expression: str = r''
		# valid scheme
		valid_url_expression += r"^(" + "|".join(scheme.value for scheme in UrlScheme) + ")://"
		# domain
		valid_url_expression += r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
		# or localhost
		valid_url_expression += r"localhost|"
		# or IP address
		valid_url_expression += r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
		# optional port number
		valid_url_expression += r"(?::\d+)?"
		# path after domain
		valid_url_expression += r"(?:/?|[/?]\S+)$"
			
		url_pattern = re.compile(
				valid_url_expression,
				re.IGNORECASE
		)

		return url_pattern.match(url) != None
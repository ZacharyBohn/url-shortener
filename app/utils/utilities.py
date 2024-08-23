import hashlib
import re
from uuid import uuid4
from pydantic import PositiveInt

from app.interfaces.url_schemes import UrlScheme
from app.interfaces.utilities_interface import IUtilities


class Utilities(IUtilities):
	def generate_random_string(self, length: int) -> str:
		if length < 1:
			return ''
		return str(uuid4())[:length]

	def hash_string(self, string: str, output_length: PositiveInt) -> str:
		hash_bytes: bytes = hashlib.sha256(string.encode()).digest()
		hex_encoded: str = hash_bytes.hex()[:output_length]
		return hex_encoded

	def is_valid_url(self, url: str) -> bool:
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
	
	def extract_short_url_id(self, short_url: str, id_length: int) -> str:
		pattern = fr'(\d{{{id_length}}})$'
		match = re.search(pattern, short_url)
		if match:
			return match.group(1)
		else:
			raise Exception(f"The URL does not contain a valid {id_length}-digit ID")
		
	def generate_short_url_from_id(
			self,
			short_url_id: str,
			scheme: UrlScheme,
			domain: str
			) -> str:
		return f"{scheme.value}://{domain}/{short_url_id}"
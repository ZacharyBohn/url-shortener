from abc import ABC, abstractmethod
from pydantic import PositiveInt

from app.interfaces.url_schemes import UrlScheme

class IUtilities(ABC):
	@abstractmethod
	def generate_random_string(self, length: int) -> str:
		pass

	@abstractmethod
	def hash_string(self, string: str, output_length: PositiveInt) -> str:
		pass

	@abstractmethod
	def is_valid_url(self, url: str) -> bool:
		pass

	@abstractmethod
	def extract_short_url_id(self, short_url: str, id_length: int) -> str:
		pass

	@abstractmethod
	def generate_short_url_from_id(
			self,
			short_url_id: str,
			scheme: UrlScheme,
			domain: str
			) -> str:
		pass
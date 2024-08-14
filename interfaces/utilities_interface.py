from abc import ABC, abstractmethod

from pydantic import PositiveInt

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
from abc import ABC, abstractmethod
from typing import Optional

from models.short_url_model import ShortUrlModel

class IDB(ABC):
	@staticmethod
	@abstractmethod
	def setup():
		pass

	@staticmethod
	@abstractmethod
	def get_all_urls() -> list[ShortUrlModel]:
		pass

	@staticmethod
	@abstractmethod
	def get_short_url(short_url_id: str) -> ShortUrlModel | None:
		pass

	@staticmethod
	@abstractmethod
	def create_short_url(
		original_url: str,
		short_url_id: Optional[str] = None,
	) -> str:
		pass
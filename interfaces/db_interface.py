from abc import ABC, abstractmethod
from typing import Optional

from models.short_url_model import ShortUrlModel

class IDB(ABC):
	@classmethod
	@abstractmethod
	def connect(cls):
		pass

	@classmethod
	@abstractmethod
	def close(cls):
		pass

	@classmethod
	@abstractmethod
	def get_all_urls(cls) -> list[ShortUrlModel]:
		pass

	@classmethod
	@abstractmethod
	def get_short_url(cls, short_url_id: str) -> ShortUrlModel | None:
		pass

	@classmethod
	@abstractmethod
	def create_short_url(
		cls,
		original_url: str,
		short_url_id: Optional[str] = None,
	) -> str:
		pass
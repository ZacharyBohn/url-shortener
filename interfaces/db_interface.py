from abc import ABC, abstractmethod
from typing import Optional

from models.short_url import ShortUrlModel

class IDb(ABC):
	@staticmethod
	@abstractmethod
	def setup():
		pass

	@staticmethod
	@abstractmethod
	async def get_urls() -> list[ShortUrlModel]:
		pass

	@staticmethod
	@abstractmethod
	async def get_original_url(short_url_id: str) -> ShortUrlModel:
		pass

	@staticmethod
	@abstractmethod
	async def create_short_url(
		original_url: str,
		short_url_id: Optional[str] = None,
	) -> str:
		pass
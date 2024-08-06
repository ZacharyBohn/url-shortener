from abc import ABC, abstractmethod
from typing import Dict

class IListUrlsService(ABC):
	@abstractmethod
	async def list_urls(self) -> Dict[str, str]:
		pass
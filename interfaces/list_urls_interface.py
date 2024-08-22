from abc import ABC, abstractmethod
from typing import Dict

class IListUrls(ABC):
	@abstractmethod
	def list_urls(self) -> Dict[str, str]:
		pass
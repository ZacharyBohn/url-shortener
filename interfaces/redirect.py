from abc import ABC, abstractmethod

class IRedirectService(ABC):
	@abstractmethod
	async def redirect(self, short_url: str) -> str:
		pass
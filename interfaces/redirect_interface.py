from abc import ABC, abstractmethod

class IRedirect(ABC):
	@abstractmethod
	async def redirect(self, short_url: str) -> str:
		pass
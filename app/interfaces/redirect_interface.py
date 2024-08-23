from abc import ABC, abstractmethod

class IRedirect(ABC):
	@abstractmethod
	def redirect(self, short_url: str) -> str | None:
		pass
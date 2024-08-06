from typing import Dict

from interfaces.list_urls import IListUrlsService

class ListUrlsService(IListUrlsService):
	async def list_urls(self) -> Dict[str, str]:
		return {}
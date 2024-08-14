from typing import Dict

from interfaces.list_urls_interface import IListUrls

class ListUrlsService(IListUrls):
	async def list_urls(self) -> Dict[str, str]:
		return {}
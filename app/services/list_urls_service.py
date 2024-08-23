from typing import Dict, List

from app.interfaces.url_schemes import UrlScheme
from app.models.short_url_model import ShortUrlModel
from app.dependency_injector.di import DI
from app.interfaces.list_urls_interface import IListUrls
from settings import domain

class ListUrlsService(IListUrls):
	def list_urls(self) -> Dict[str, str]:
		db = DI.instance().db
		utils = DI.instance().utils
		short_urls: List[ShortUrlModel] = db.get_all_urls()
		all_urls: Dict[str, str] = {}
		for short_url in short_urls:
			full_short_url = utils.generate_short_url_from_id(
				short_url.id,
				UrlScheme.HTTPS,
				domain)
			all_urls[full_short_url] = short_url.original_url
		return all_urls
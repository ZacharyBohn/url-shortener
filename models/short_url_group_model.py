from typing import List
from pydantic import BaseModel

from models.short_url_model import ShortUrlModel

class ShortUrlGroupModel(BaseModel):
	id: str
	url_pairs: List[ShortUrlModel] = []

	# def __init__(self, id: str, url_pairs: List[ShortUrlModel] = []) -> None:
	# 	super().__init__(id=id, url_pairs=url_pairs)
	# 	self.id = id
	# 	self.url_pairs = url_pairs or []
	# 	return

	def get_short_url_model(self, short_url_id: str) -> ShortUrlModel | None:
		for short_url in self.url_pairs:
			if short_url.id == short_url_id:
				return short_url
		return None
			
	def contains_short_url_id(self, short_url_id: str) -> bool:
		for short_url in self.url_pairs:
			if short_url.id == short_url_id:
				return True
		return False

	def add_short_url(self, short_url: ShortUrlModel):
		self.url_pairs.append(short_url)
		return

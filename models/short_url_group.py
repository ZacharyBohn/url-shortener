from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute

from models.short_url import ShortUrlModel

class ShortUrlGroupModel(Model):
	class Meta: # type: ignore
		table_name: str = 'shorten_urls'
	id: UnicodeAttribute = UnicodeAttribute(hash_key=True)
	url_pairs: ListAttribute[ShortUrlModel] = ListAttribute(of=ShortUrlModel)
			
	def contains_short_url_id(self, short_url_id: str) -> bool:
		for short_url in self.url_pairs:
			if short_url.id == short_url_id:
				return True
		return False

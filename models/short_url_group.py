from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute

from models.short_url import ShortUrlModel

class ShortUrlGroupModel(Model):
    class Meta: # type: ignore
        table_name: str = 'shorten_urls'
    id: UnicodeAttribute = UnicodeAttribute(hash_key=True)
    original_urls: ListAttribute[ShortUrlModel] = ListAttribute(of=ShortUrlModel)

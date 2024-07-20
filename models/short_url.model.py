from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

class ShortUrlModel(Model):
    class Meta: # type: ignore
        table_name: str = 'Thread'
    id: UnicodeAttribute = UnicodeAttribute(hash_key=True)
    original_url: UnicodeAttribute = UnicodeAttribute()
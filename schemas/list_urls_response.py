from typing import Dict
from pydantic import BaseModel

class ListUrlsResponse(BaseModel):
	# short url: original url
	short_urls: Dict[str, str]
from typing import Dict
from pydantic import BaseModel

class ListUrlsResponse(BaseModel):
	short_urls: Dict[str, str]
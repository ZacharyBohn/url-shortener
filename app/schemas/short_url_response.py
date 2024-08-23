from pydantic import BaseModel

class ShortUrlResponse(BaseModel):
	short_url: str
	original_url: str
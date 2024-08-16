from pydantic import BaseModel

class ShortUrlModel(BaseModel):
	id: str
	original_url: str

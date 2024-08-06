from pydantic import BaseModel

class RedirectResponse(BaseModel):
	original_url: str
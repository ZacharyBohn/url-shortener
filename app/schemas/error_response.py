from pydantic import BaseModel

class ErrorReponse(BaseModel):
	error: str
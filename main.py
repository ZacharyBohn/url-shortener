from fastapi import FastAPI

from api import list_urls
from api import redirect
from api import shorten_url

# TODO: fill in with the actual domain
domain: str = 'domain.com'
short_id_length: int = 6

def create_app() -> FastAPI:
	app = FastAPI()
	app.include_router(list_urls.router)
	app.include_router(redirect.router)
	app.include_router(shorten_url.router)

	@app.get('/ping')
	def ping(): # type: ignore
		return 'ok'
	return app

if __name__ == "__main__":
	app = create_app()
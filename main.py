from fastapi import FastAPI

from api import list_urls
from api import redirect
from api import shorten_url

app = FastAPI()

# TODO: fill in with the actual domain
domain: str = 'domain.com'
short_id_length: int = 6

app.include_router(list_urls.router)
app.include_router(redirect.router)
app.include_router(shorten_url.router)

@app.get('/ping')
def ping():
	return 'ok'
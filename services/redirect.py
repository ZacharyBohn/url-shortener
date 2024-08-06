from ..interfaces.redirect import IRedirectService


class RedirectService(IRedirectService):
	async def redirect(self, short_url: str) -> str:
		return ''

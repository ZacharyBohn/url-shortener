from interfaces.redirect_interface import IRedirect


class RedirectService(IRedirect):
	async def redirect(self, short_url: str) -> str:
		return ''

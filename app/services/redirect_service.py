from app.dependency_injector.di import DI
from app.interfaces.redirect_interface import IRedirect
from app.models.short_url_model import ShortUrlModel
from app.settings import short_id_length

class RedirectService(IRedirect):
	def redirect(self, short_url: str) -> str | None:
		db = DI.instance().db
		utils = DI.instance().utils
		short_url_id = utils.extract_short_url_id(short_url, short_id_length)
		short_url_model: ShortUrlModel | None = db.get_short_url(short_url_id)
		if short_url_model is None: return None
		return short_url_model.original_url

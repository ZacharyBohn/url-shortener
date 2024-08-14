from dependency_injector.di_defaults import set_di_production_defaults
from db.db import Db
from models.short_url import ShortUrlModel
from models.short_url_group import ShortUrlGroupModel
from exceptions.exceptions import UnavailableUrlException
from utils.utilities import Utilities
from dependency_injector.di import DI
from services.shorten_url_service import ShortenUrlService, InvalidUrlException
import unittest

from main import domain, short_id_length

class TestUrlShortener(unittest.TestCase):
	def setUp(self) -> None:
		DI.reset()
		set_di_production_defaults()
		return super().setUp()

	def test_valid_url_shortener(self):
		original_url: str = 'http://original.com/long-url'
		short_url = ShortenUrlService().shorten_url(
			original_url,
			)
		short_url_length = len(f'http://{domain}/') + short_id_length
		self.assertTrue(type(short_url) is str and len(short_url) == short_url_length)
		return
		
	def test_valid_url_with_ftp_shortener(self):
		original_url: str = 'ftp://original.com/long-url'
		short_url = ShortenUrlService().shorten_url(
			original_url,
			)
		short_url_length = len(f'http://{domain}/') + short_id_length
		self.assertTrue(type(short_url) is str and len(short_url) == short_url_length)
		return
		
	def test_valid_url_with_params_shortener(self):
		short_url = ShortenUrlService().shorten_url(
			'http://domain.com/?name=John&age=30',
			)
		short_url_length = len(f'http://{domain}/') + short_id_length
		self.assertTrue(type(short_url) is str and len(short_url) == short_url_length)
		return
		
	async def test_invalid_url_shortener(self):
		with self.assertRaises(InvalidUrlException):
			await ShortenUrlService().shorten_url(
			'invalid_scheme://domain.com/',
			)
		return
		
	def test_shorten_url_with_collisions(self):
		# monkey wrench the utility function to force collisions
		# during the first time it's called
		class _IsFirstGenerationCall:
			value = True
		def collision_string(length: int) -> str:
			if _IsFirstGenerationCall.value:
				return '0' * length
			# after the first call has been intercepted,
			# just generate random strings as before
			return Utilities().generate_random_string(length)
		force_collision_utilities: Utilities = Utilities()
		force_collision_utilities.generate_random_string = collision_string

		# force the database to think there is a collision
		async def _get_url_group_preset(url_group_id: str) -> ShortUrlGroupModel | None:
			return ShortUrlGroupModel(
				url_pairs=[
					ShortUrlModel(
						id='0' * short_id_length,
						original_url='http://domain.com/'
					),
				]
				)
		force_collision_db: Db = Db()
		force_collision_db._get_url_group = _get_url_group_preset # type: ignore
		
		DI.instance().utils = force_collision_utilities
		DI.instance().db = force_collision_db

		short_url = ShortenUrlService().shorten_url(
			"http://domain.com/link-to-some-page"
			)
		short_url_length = len(f"http://{domain}/") + short_id_length
		self.assertTrue(type(short_url) is str and len(short_url) == short_url_length)
		return
		
	def test_shorten_url_with_custom_url(self):
		original_url: str = 'http://original.com/long-url'
		short_url = ShortenUrlService().shorten_url(
			original_url,
			''
			)
		short_url_length = len(f'http://{domain}/') + short_id_length
		self.assertTrue(type(short_url) is str and len(short_url) == short_url_length)
		return
		
	async def test_shorten_url_with_collisions_and_custom_url(self):
		# monkey wrench the utility function to force collisions
		# counter is used so that when it tries to regenerate a
		# new string after a collision, a new one will be generated.
		# list is used for maintaining state across function calls
		counter: list[int] = [0]
		force_collision_utilities: Utilities = Utilities()
		def collision_string(length: int) -> str:
			counter[0] += 1
			return f'{counter[0]}' * length
		force_collision_utilities.generate_random_string = collision_string
		DI.instance().utils = force_collision_utilities

		with self.assertRaises(UnavailableUrlException):
			await ShortenUrlService().shorten_url(
				"http://domain.com/link-to-some-page",
				f"http://{domain}/{'0' * short_id_length}"
				)
		return

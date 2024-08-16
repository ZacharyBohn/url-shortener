from database.db import DB
from exceptions.exceptions import UnavailableUrlException
from services.redirect_service import RedirectService
from services.list_urls_service import ListUrlsService
from utils.utilities import Utilities
from dependency_injector.di import DI
from services.shorten_url_service import ShortenUrlService, InvalidUrlException
import unittest

from main import domain, short_id_length

class TestUrlShortener(unittest.TestCase):
	def setUp(self) -> None:
		DI.reset()
		DI(
			list_urls_service=ListUrlsService(),
			redirect_service=RedirectService(),
			shorten_url_service=ShortenUrlService(),
			utils=Utilities(),
			db=DB,
		)
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
		
	def test_invalid_url_shortener(self):
		with self.assertRaises(InvalidUrlException):
			ShortenUrlService().shorten_url(
			'invalid_scheme://domain.com/',
			)
		return
		
	def test_shorten_url_with_collisions(self):
		# TODO: create a short url id that collides
		# short_url = DB.create_short_url('http://original.com/long-url', '0' * short_id_length)
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
		
	def test_shorten_url_with_collisions_and_custom_url(self):
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
			ShortenUrlService().shorten_url(
				"http://domain.com/link-to-some-page",
				f"http://{domain}/{'0' * short_id_length}"
				)
		return

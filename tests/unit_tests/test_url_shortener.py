import unittest
from moto import mock_aws

from app.database.db import DB
from app.services.redirect_service import RedirectService
from app.services.list_urls_service import ListUrlsService
from app.utils.utilities import Utilities
from app.dependency_injector.di import DI
from app.services.shorten_url_service import ShortenUrlService, InvalidUrlException
from app.settings import domain, short_id_length

@mock_aws
class TestUrlShortener(unittest.TestCase):
	def setUp(self) -> None:
		di = DI(
			list_urls_service=ListUrlsService(),
			redirect_service=RedirectService(),
			shorten_url_service=ShortenUrlService(),
			utils=Utilities(),
			db=DB,
		)
		di.db.connect()
		di.db.create_table(di.db.shorten_urls_table_name)
		return
	
	def tearDown(self) -> None:
		DI.instance().db.close()
		DI.reset()
		return
	
	def test_valid_url_shortener(self):
		original_url: str = 'https://original.com/long-url'
		short_url = ShortenUrlService().shorten_url(
			original_url,
			)
		short_url_length = len(f'https://{domain}/') + short_id_length
		self.assertTrue(type(short_url) is str and len(short_url) == short_url_length)
		return
		
	def test_valid_url_with_ftp_shortener(self):
		original_url: str = 'ftp://original.com/long-url'
		short_url = ShortenUrlService().shorten_url(
			original_url,
			)
		short_url_length = len(f'https://{domain}/') + short_id_length
		self.assertTrue(type(short_url) is str and len(short_url) == short_url_length)
		return
		
	def test_valid_url_with_params_shortener(self):
		short_url = ShortenUrlService().shorten_url(
			'http://domain.com/?name=John&age=30',
			)
		short_url_length = len(f'https://{domain}/') + short_id_length
		self.assertTrue(type(short_url) is str and len(short_url) == short_url_length)
		return
		
	def test_invalid_url_shortener(self):
		with self.assertRaises(InvalidUrlException):
			ShortenUrlService().shorten_url(
			'invalid_scheme://domain.com/',
			)
		return
		
	def test_shorten_url_with_custom_url(self):
		original_url: str = 'http://original.com/long-url'
		short_url = ShortenUrlService().shorten_url(
			original_url,
			'556556'
			)
		short_url_length = len(f'https://{domain}/') + short_id_length
		self.assertTrue(type(short_url) is str and len(short_url) == short_url_length)
		return

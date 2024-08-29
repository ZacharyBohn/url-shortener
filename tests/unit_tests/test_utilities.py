import unittest

from app.interfaces.url_schemes import UrlScheme
from app.utils.utilities import Utilities

class TestUtilities(unittest.TestCase):
	
	def test_generate_random_string(self):
		utils = Utilities()
		length: int = 5
		random_string: str = utils.generate_random_string(length)
		self.assertEqual(len(random_string), length)

		length = 12
		random_string = utils.generate_random_string(length)
		self.assertEqual(len(random_string), length)
		return

	def test_hash_string(self):
		utils = Utilities()
		original_string: str = 'Test String'
		output_length: int = 5
		hash_value: str = utils.hash_string(original_string, output_length)
		hash_value2: str = utils.hash_string(original_string, output_length)
		self.assertEqual(hash_value, hash_value2)
		return

	def test_is_valid_url(self):
		utils = Utilities()
		valid_url1: str = 'http://domain.com/some-link'
		valid_url2: str = 'https://otherdomain.com/some-other-link'
		valid_url3: str = 'ftp://abc.org'
		self.assertTrue(utils.is_valid_url(valid_url1))
		self.assertTrue(utils.is_valid_url(valid_url2))
		self.assertTrue(utils.is_valid_url(valid_url3))
		return

	def test_is_invalid_url(self):
		utils = Utilities()
		invalid_url1: str = 'http://.com/some-link'
		invalid_url2: str = 'hpx://otherdomain.com/some-other-link'
		invalid_url3: str = 'ftp://abc_domain.com'
		self.assertFalse(utils.is_valid_url(invalid_url1))
		self.assertFalse(utils.is_valid_url(invalid_url2))
		self.assertFalse(utils.is_valid_url(invalid_url3))
		return
	
	def test_extract_short_url_id(self):
		utils = Utilities()
		short_url_id: str = 'H93x89aa'
		short_url: str = f'https://domain.com/{short_url_id}'
		self.assertEqual(utils.extract_short_url_id(short_url, 8), short_url_id)
		return
		
	def test_generate_short_url_from_id(self):
		utils = Utilities()
		domain: str = 'domain.com'
		scheme: UrlScheme = UrlScheme.HTTPS
		short_url_id: str = 'H93x89aa'
		short_url: str = f'{scheme.value}://{domain}/{short_url_id}'
		self.assertEqual(
			utils.generate_short_url_from_id(
				short_url_id,
				scheme,
				domain,
				),
			short_url
			)
		return
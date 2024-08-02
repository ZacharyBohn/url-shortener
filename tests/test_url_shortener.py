import service.shorten_url as shorten_url
import unittest

class TestUrlShortener(unittest.TestCase):
	def test_valid_url_shortener(self):
		short_url = shorten_url.generate_short_url(
			'http://domain.com/',
			)
		self.assertTrue(type(short_url) is str)
		return
		
	def test_valid_url_with_ftp_shortener(self):
		short_url = shorten_url.generate_short_url(
			'ftp://domain.com/',
			)
		self.assertTrue(type(short_url) is str)
		return
		
	def test_valid_url_with_params_shortener(self):
		short_url = shorten_url.generate_short_url(
			'http://domain.com/?name=John&age=30',
			)
		self.assertTrue(type(short_url) is str)
		return
		
	def test_invalid_url_shortener(self):
		with self.assertRaises(shorten_url.InvalidUrlException):
			shorten_url.generate_short_url(
			'invalid_scheme://domain.com/',
			)
		return
		
	def test_url_generates_to_the_same(self):
		short_url1 = shorten_url.generate_short_url(
			'http://domain.com/',
			)
		
		short_url2 = shorten_url.generate_short_url(
			'http://domain.com/',
			)
		
		self.assertEqual(short_url1, short_url2)
		return
import url_shortener
import unittest

class UrlShortenerTests(unittest.TestCase):
  def test_valid_url_shortener(self):
    short_url = url_shortener.generate_short_url(
      'http://domain.com/',
      6,
      url_shortener.UrlScheme.HTTPS,
      'myweb.com',
      )
    self.assertTrue(type(short_url) is str)
    return
  
  def test_invalid_url_shortener(self):
    with self.assertRaises(url_shortener.InvalidUrlException):
      url_shortener.generate_short_url(
      'invalid_scheme://domain.com/',
      6,
      url_shortener.UrlScheme.HTTPS,
      'myweb.com',
      )
    return
  
  def test_url_generates_to_the_same(self):
    short_url1 = url_shortener.generate_short_url(
      'http://domain.com/',
      6,
      url_shortener.UrlScheme.HTTPS,
      'myweb.com',
      )
    
    short_url2 = url_shortener.generate_short_url(
      'http://domain.com/',
      6,
      url_shortener.UrlScheme.HTTPS,
      'myweb.com',
      )
    
    self.assertEquals(short_url1, short_url2)
    return

unittest.main()
import unittest
from fastapi.testclient import TestClient
from httpx import Response

from main import app, domain, short_id_length

client = TestClient(app)

class TestApis(unittest.TestCase):
  def test_shorten_url(self):
    original_url: str = 'http://domain.com/link-to-my-page'
    response: Response = client.post(
      '/shorten_url',
      params={
        'url': original_url,
        },
      )
    json = response.json()
    first_part = f'https://{domain}/'
    self.assertEqual(json[:len(first_part)], first_part)
    self.assertEqual(len(json[len(first_part):]), short_id_length)
    return
  
  def test_list_urls(self):
    self.assertTrue(True)
    return
  
  def test_redirect(self):
    self.assertTrue(True)
    return
import unittest
from fastapi.testclient import TestClient
from httpx import Response

from db.db import Db
from utils.utilities import Utilities
from dependency_injector.di import DI
from main import create_app, domain, short_id_length


class TestApis(unittest.TestCase):
	"""
	Test without collisions, no custom URL
	Description: We pass in a long URL, we will expect a short URL to
	be returned. We will need to test if the URL is written to the DB.
	"""
	def test_shorten_url(self):
		client = TestClient(create_app())
		original_url: str = "http://other_domain.com/link-to-my-page"
		response: Response = client.post(
			"/shorten_url",
			params={
				"url": original_url,
			},
		)
		short_url_response = response.json()
		# first part of the short url that should be generated
		first_part = f"https://{domain}/"
		self.assertEqual(short_url_response[: len(first_part)], first_part)
		self.assertEqual(len(short_url_response[len(first_part) :]), short_id_length)
		self.assertEqual(Db.get_original_url(short_url_response), original_url)
		return

	def test_shorten_url_with_collisions(self):
		client = TestClient(create_app())
		force_collision_utilities: Utilities = Utilities()
		def collision_string(length: int) -> str:
			return '0' * length
		force_collision_utilities.generate_random_string = collision_string
		DI(utils=force_collision_utilities)
		original_url: str = "http://other_domain.com/link-to-my-page"
		response: Response = client.post(
				"/shorten_url",
				params={
					"url": original_url,
				},
			)
			
		short_url_response = response.json()
		# first part of the short url that should be generated
		first_part = f"https://{domain}/"
		self.assertEqual(short_url_response[: len(first_part)], first_part)
		self.assertEqual(len(short_url_response[len(first_part) :]), short_id_length)
		self.assertEqual(Db.get_original_url(short_url_response), original_url)
		return

	def test_shorten_url_with_custom_url(self):
		self.assertTrue(True)
		return

	"""
 Test without collisions, with custom URL
Description: Same as the first positive test case, except now we pass in a custom URL that will not yield a collision.
	"""

	def test_shorten_url_with_custom_url_and_collisions(self):
		self.assertTrue(True)
		return

	"""
 Test with collision, with custom URL
Description: We pass in a long URL with a custom URL. Because it's a customer URL, we cannot regenerate, and therefore we will return an error to the user
	"""

	def test_shorten_url_invalid_custom_url(self):
		self.assertTrue(True)
		return

	"""
 Test giving a short URL that is found in the DB:
Description: We create a short URL in the DB. Then we ask the system for the original URL by giving it a short URL. The system should return the original URL.
	"""

	def test_list_urls(self):
		self.assertTrue(True)
		return

	"""
 Test giving a short URL that is not found in the DB:
Description: We ask the system to give us the original URL and give it a short URL that does not exist in the DB. The system should return an error and say that the short URL is invalid.
	"""

	def test_redirect(self):
		self.assertTrue(True)
		return

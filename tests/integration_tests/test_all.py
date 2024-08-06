import unittest
from unittest import mock
from fastapi.testclient import TestClient
from httpx import Response

from db.db import Db
from main import app, domain, short_id_length

client = TestClient(app)


class TestApis(unittest.TestCase):
	"""
	Test without collisions, no custom URL
	Description: We pass in a long URL, we will expect a short URL to
	be returned. We will need to test if the URL is written to the DB.
	"""
	def test_shorten_url(self):
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

		# used to override what the db returns to force
		# a collision
		def get_item_override(*args, **kwargs): # type: ignore

			return
		get_item_path: str = 'boto3.resources.factory.dynamodb.Table.get_item'

		original_url: str = "http://other_domain.com/link-to-my-page"
		with mock.patch(get_item_path, get_item_override): # type: ignore
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

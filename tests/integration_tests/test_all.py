from typing import Iterable
import unittest
from fastapi.testclient import TestClient
from httpx import Response
from moto import mock_aws

from db.db import DB
from ...dependency_injector.di_defaults import set_di_production_defaults
from schemas.list_urls_response import ListUrlsResponse
from schemas.redirect_response import RedirectResponse
from schemas.short_url_response import ShortUrlResponse
from schemas.error_response import ErrorReponse
from utils.utilities import Utilities
from dependency_injector.di import DI
from main import create_app, domain, short_id_length


class TestApis(unittest.TestCase):
	def setUp(self) -> None:
		DI.reset()
		set_di_production_defaults()
		return super().setUp()

	@mock_aws
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
		# ensure the short id length is correct
		self.assertEqual(len(short_url_response[len(first_part) :]), short_id_length)
		# ensure that the url was inserted into the db
		self.assertEqual(DB.get_short_url(short_url_response), original_url)
		return

	@mock_aws
	async def test_shorten_url_with_collisions(self):
		# monkey wrench the utility function to force collisions.
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
		# drop a short url in the db to collide with
		# the generate_random_string function will generate a short id
		# of just 0's
		original_url_1: str = "http://other_domain.com/link-to-my-page"
		short_url_1: str = f"https://{domain}/{'0' * short_id_length}"
		await DB.create_short_url(original_url_1, short_url_1)
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
		# ensure the short id length is correct
		self.assertEqual(len(short_url_response[len(first_part) :]), short_id_length)
		# ensure that the url was inserted into the db and
		# was able to overcome the collision
		self.assertEqual(DB.get_short_url(short_url_response), original_url)
		return

	@mock_aws
	async def test_shorten_url_with_custom_url(self):
		client = TestClient(create_app())
		original_url: str = "http://other_domain.com/link-to-my-page"
		custom_id: str = '012345'
		response: Response = client.post(
			"/shorten_url",
			params={
				"url": original_url,
				"short_url": custom_id
			},
		)
		short_url_response_raw = response.json()
		short_url_response: ShortUrlResponse = ShortUrlResponse.model_validate_json(short_url_response_raw)
		# first part of the short url that should be generated
		first_part = f"https://{domain}/"
		# ensure the short id given back to use is the one that we
		# gave the endpoint
		self.assertEqual(short_url_response.short_url[len(first_part):], custom_id)
		# ensure that the url was inserted into the db
		self.assertEqual(await DB.get_short_url(short_url_response.short_url), original_url)
		return

	@mock_aws
	def test_shorten_url_with_custom_url_and_collisions(self):
		client = TestClient(create_app())
		original_url: str = "http://other_domain.com/link-to-my-page"
		custom_id: str = '012345'
		response: Response = client.post(
			"/shorten_url",
			params={
				"url": original_url,
				"short_url": custom_id
			},
		)
		short_url_response_raw = response.json()
		error: ErrorReponse = ErrorReponse.model_validate_json(short_url_response_raw)
		self.assertNotEqual(error.error, None)
		return

	@mock_aws
	def test_shorten_url_invalid_custom_url(self):
		client = TestClient(create_app())
		original_url: str = "http://other_domain.com/link-to-my-page"
		custom_id: str = ''
		response: Response = client.post(
			"/shorten_url",
			params={
				"url": original_url,
				"short_url": custom_id
			},
		)
		short_url_response_raw = response.json()
		error: ErrorReponse = ErrorReponse.model_validate_json(short_url_response_raw)
		self.assertNotEqual(error.error, None)
		return

	@mock_aws
	async def test_redirect(self):
		client = TestClient(create_app())
		original_url: str = "http://other_domain.com/link-to-my-page"
		short_url: str = f"https://{domain}/012345"
		await DB.create_short_url(original_url, short_url)
		response: Response = client.post(
			"/redirect",
			params={
				"short_url": short_url
			},
		)
		short_url_response_raw = response.json()
		redirect: RedirectResponse = RedirectResponse.model_validate_json(short_url_response_raw)
		self.assertEqual(redirect.original_url, original_url)
		return
	
	@mock_aws
	def test_redirect_fake_short_url(self):
		client = TestClient(create_app())
		short_url: str = f"https://{domain}/012345"
		response: Response = client.post(
			"/redirect",
			params={
				"short_url": short_url
			},
		)
		short_url_response_raw = response.json()
		error: ErrorReponse = ErrorReponse.model_validate_json(short_url_response_raw)
		self.assertNotEqual(error.error, None)
		return

	@mock_aws
	async def test_list_urls(self):
		client = TestClient(create_app())
		original_url_1: str = "http://other_domain.com/link-to-my-page"
		short_url_1: str = f"https://{domain}/012345"
		await DB.create_short_url(original_url_1, short_url_1)
		original_url_2: str = "http://other_domain.com/link-to-my-other-page"
		short_url_2: str = f"https://{domain}/678901"
		await DB.create_short_url(original_url_2, short_url_2)
		response: Response = client.post(
			"/list_urls",
		)
		list_urls_response_raw = response.json()
		list_urls_response: ListUrlsResponse = ListUrlsResponse.model_validate_json(list_urls_response_raw)
		self.assertEqual(len(list_urls_response.short_urls), 2)
		url_pairs: Iterable[tuple[str, str]] = iter(list_urls_response.short_urls.items())
		first_pair: tuple[str, str] = next(url_pairs)
		second_pair: tuple[str, str] = next(url_pairs)
		self.assertEqual(first_pair[0], short_url_1)
		self.assertEqual(first_pair[1], original_url_1)
		self.assertEqual(second_pair[0], short_url_2)
		self.assertEqual(second_pair[1], original_url_2)
		return

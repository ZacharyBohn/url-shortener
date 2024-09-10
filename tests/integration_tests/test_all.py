import unittest
from fastapi.testclient import TestClient
from httpx import Response
from moto import mock_aws

from app.database.db import DB
from app.interfaces.logger_interface import LogLevel
from app.schemas.list_urls_response import ListUrlsResponse
from app.schemas.redirect_response import RedirectResponse
from app.schemas.error_response import ErrorReponse
from app.schemas.short_url_response import ShortUrlResponse
from app.services.shorten_url_service import ShortenUrlService
from app.services.redirect_service import RedirectService
from app.services.list_urls_service import ListUrlsService
from app.utils.utilities import Utilities
from app.dependency_injector.di import DI
from app.utils.logger import Logger
from main import create_app
from settings import domain, short_id_length

@mock_aws
class TestApis(unittest.TestCase):
	def setUp(self) -> None:
		di = DI(
			list_urls_service=ListUrlsService(),
			redirect_service=RedirectService(),
			shorten_url_service=ShortenUrlService(),
			utils=Utilities(),
			db=DB,
			logger=Logger("tests")
		)
		di.logger.setLogLevel(LogLevel.ERROR)
		di.db.connect()
		di.db.create_table(di.db.shorten_urls_table_name)
		return
	
	def tearDown(self) -> None:
		DI.instance().db.close()
		DI.reset()
		return
	
	def test_shorten_url(self):
		client = TestClient(create_app())
		original_url: str = "https://otherdomain.com/link-to-my-page"
		response: Response = client.post(
			"/shorten_url",
			params={
				"url": original_url,
			},
		)
		self.assertEqual(response.status_code, 200)
		short_url_response = ShortUrlResponse.model_validate(response.json())
		first_part = f"https://{domain}/"
		first_part_len = len(first_part)
		second_part = short_url_response.short_url[first_part_len:]
		second_part_len = len(second_part)
		self.assertEqual(second_part_len, short_id_length)

		# ensure that the url was inserted into the db
		db = DI.instance().db
		db_short_url = db.get_short_url(second_part)
		self.assertNotEqual(db_short_url, None)
		if db_short_url is None: raise Exception() # just for typing
		self.assertEqual(db_short_url.original_url, original_url)
		return

	def test_shorten_url_with_collisions(self):
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
		original_url_1: str = "https://otherdomain.com/link-to-my-page"
		short_url_1: str = f"https://{domain}/{'0' * short_id_length}"
		DB.create_short_url(original_url_1, short_url_1)
		client = TestClient(create_app())
		original_url: str = "https://otherdomain.com/link-to-my-page"
		response: Response = client.post(
				"/shorten_url",
				params={
					"url": original_url,
				},
			)
		self.assertEqual(response.status_code, 200)
		short_url_response = ShortUrlResponse.model_validate(response.json())
		first_part = f"https://{domain}/"
		first_part_len = len(first_part)
		second_part = short_url_response.short_url[first_part_len:]
		second_part_len = len(second_part)
		self.assertEqual(second_part_len, short_id_length)
		db = DI.instance().db
		db_short_url = db.get_short_url(second_part)
		self.assertNotEqual(db_short_url, None)
		if db_short_url is None: raise Exception() # just for typing
		self.assertEqual(db_short_url.original_url, original_url)
		return
	
	def test_shorten_url_with_custom_url(self):
		client = TestClient(create_app())
		original_url: str = "https://otherdomain.com/link-to-my-page"
		custom_id: str = '012345'
		response: Response = client.post(
			"/shorten_url",
			params={
				"url": original_url,
				"short_url_id": custom_id
			},
		)
		json = response.json()
		short_url_response = ShortUrlResponse.model_validate(json)
		# first part of the short url that should be generated
		first_part = f"https://{domain}/"
		first_part_len = len(first_part)
		second_part = short_url_response.short_url[first_part_len:]
		# ensure the short id given back to use is the one that we
		# gave the endpoint
		self.assertEqual(second_part, custom_id)
		# ensure that the url was inserted into the db
		db = DI.instance().db
		db_short_url = db.get_short_url(second_part)
		self.assertNotEqual(db_short_url, None)
		if db_short_url is None: raise Exception() # just for typing
		self.assertEqual(db_short_url.original_url, original_url)
		return
	
	def test_shorten_url_with_custom_url_and_collisions(self):
		# drop a short url in the db to collide with
		# the given custom url
		original_url_1: str = "https://otherdomain.com/link-to-my-page"
		custom_id: str = "789123"
		db = DI.instance().db
		db.create_short_url(original_url_1, custom_id)

		client = TestClient(create_app())
		original_url: str = "http://otherdomain.com/link-to-my-other-page"
		response: Response = client.post(
			"/shorten_url",
			params={
				"url": original_url,
				"short_url_id": custom_id
			},
		)
		json = response.json()
		error = ErrorReponse.model_validate(json)
		self.assertNotEqual(error.error, None)
		return
	
	def test_shorten_url_invalid_custom_url(self):
		client = TestClient(create_app())
		original_url: str = "http://other_domain.com/link-to-my-page"
		custom_id: str = ''
		response: Response = client.post(
			"/shorten_url",
			params={
				"url": original_url,
				"short_url_id": custom_id
			},
		)
		self.assertEqual(response.status_code, 400)
		json = response.json()
		error: ErrorReponse = ErrorReponse.model_validate(json)
		self.assertNotEqual(error.error, None)
		return
	
	def test_redirect(self):
		client = TestClient(create_app())
		original_url: str = "https://otherdomain.com/link-to-my-page"
		short_url_id: str = "464646"
		short_url: str = f"https://{domain}/{short_url_id}"
		DB.create_short_url(original_url, short_url_id)
		response: Response = client.get(
			"/redirect",
			params={
				"short_url": short_url
			},
		)
		self.assertEqual(response.status_code, 200)
		json = response.json()
		redirect = RedirectResponse.model_validate(json)
		self.assertEqual(redirect.original_url, original_url)
		return
	
	def test_redirect_fake_short_url(self):
		client = TestClient(create_app())
		short_url_id: str = "949494"
		short_url: str = f"https://{domain}/{short_url_id}"
		response: Response = client.get(
			"/redirect",
			params={
				"short_url": short_url
			},
		)
		self.assertEqual(response.status_code, 400)
		json = response.json()
		error: ErrorReponse = ErrorReponse.model_validate(json)
		self.assertNotEqual(error.error, None)
		return
	
	def test_list_urls(self):
		client = TestClient(create_app())
		original_url_1: str = "https://otherdomain.com/link-to-my-page"
		short_url_id_1: str = "212121"
		short_url_1: str = f"https://{domain}/{short_url_id_1}"
		DB.create_short_url(original_url_1, short_url_id_1)
		original_url_2: str = "https://otherdomain.com/link-to-my-other-page"
		short_url_id_2: str = "678901"
		short_url_2: str = f"https://{domain}/{short_url_id_2}"
		DB.create_short_url(original_url_2, short_url_id_2)
		response: Response = client.get(
			"/list_urls",
		)
		json = response.json()
		list_urls_response = ListUrlsResponse.model_validate(json)
		# TODO: may need to clear the db?
		self.assertEqual(len(list_urls_response.short_urls), 2)
		url_pairs = list_urls_response.short_urls
		self.assertEqual(url_pairs[short_url_1], original_url_1)
		self.assertEqual(url_pairs[short_url_2], original_url_2)
		return

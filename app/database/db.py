from typing import List, Optional
from pydantic import ValidationError

from exceptions.exceptions import ShortUrlAlreadyExistsException
from database.pynamo_db import PynamoDB
from dependency_injector.di import DI
from interfaces.db_interface import IDB
from models.short_url_model import ShortUrlModel
from models.short_url_group_model import ShortUrlGroupModel
from settings import short_id_length


class DB(IDB, PynamoDB):
	_group_id_length: int = 8
	shorten_urls_table_name: str = "shorten_urls"

	@classmethod
	def connect(cls):
		cls.open_connection()
		return

	@classmethod
	def close(cls):
		cls.close_connection()
		return

	@classmethod
	def get_all_urls(cls) -> List[ShortUrlModel]:
		"""
		Returns all url pairs in the db
		"""
		all_urls: List[ShortUrlModel] = []
		for group in cls._scan_table(cls.shorten_urls_table_name):
			try:
				group_model = ShortUrlGroupModel(**group)
				for short_url in group_model.url_pairs:
					all_urls.append(short_url)
			except ValidationError as e:
				print(f'Failed to validate db json data in DB.get_all_urls(): {e}')
		return all_urls

	@classmethod
	def create_short_url(
		cls,
		original_url: str,
		short_url_id: Optional[str] = None,
	) -> str:
		"""
		Returns the id of the short url, not the full
		short url since that depends on domain and scheme.

		This function handles collisions of group id in
		the database automatically.
		"""
		if short_url_id is not None:
			return cls._create_short_url_custom_id(original_url, short_url_id)

		utils = DI.instance().utils
		while True:
			short_url_id = utils.generate_random_string(short_id_length)
			group_id: str = utils.hash_string(
				short_url_id, cls._group_id_length)
			group: ShortUrlGroupModel | None = cls._get_url_group(group_id)
			if group == None: group = ShortUrlGroupModel(id=group_id)
			# Need to continue to generate a new string and check if
			# it already exists in the db until we get a actually unique one.
			# Collision occurrence should be very low, like one in 100 trillion.
			if not group.contains_short_url_id(short_url_id): break
		group.url_pairs.append(
			ShortUrlModel(
				id=short_url_id,
				original_url=original_url,
			)
		)
		if not cls._save_url_group(group):
			raise Exception('Failed to save item')
		return short_url_id

	@classmethod
	def get_short_url(cls, short_url_id: str) -> ShortUrlModel | None:
		utils = DI.instance().utils
		group_id: str = utils.hash_string(short_url_id, cls._group_id_length)
		group: ShortUrlGroupModel | None = cls._get_url_group(group_id)
		if group is None: return None
		return group.get_short_url_model(short_url_id)

	@classmethod
	def _create_short_url_custom_id(
		cls,
		original_url: str,
		short_url_id: str,
	) -> str:
		utils = DI.instance().utils
		group_id: str = utils.hash_string(
			short_url_id, cls._group_id_length
			)
		group: ShortUrlGroupModel | None = cls._get_url_group(group_id)
		if group == None:
			group = ShortUrlGroupModel(id=group_id)
		if group.contains_short_url_id(short_url_id):
			raise ShortUrlAlreadyExistsException()

		group.url_pairs.append(
			ShortUrlModel(
				id=short_url_id,
				original_url=original_url,
			)
		)
		cls._save_url_group(group)
		return short_url_id

	@classmethod
	def _get_url_group(cls, url_group_id: str) -> ShortUrlGroupModel | None:
		"""
		Returns either the group associated with the group id
		or None if it doesn't exist
		"""
		json = cls._get_item(cls.shorten_urls_table_name, url_group_id)
		if json is None: return None
		try:
			model = ShortUrlGroupModel(**json)
			return model
		except ValidationError as e:
			print(f'Failed to convert url group model: {e}')
			return None
	
	@classmethod
	def _save_url_group(cls, group: ShortUrlGroupModel) -> bool:
		return cls._put_item(cls.shorten_urls_table_name, group.model_dump())
	
	@classmethod
	def create_table(cls, table_name: str) -> bool:
		return cls._create_table(table_name)

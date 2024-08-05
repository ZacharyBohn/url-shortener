import boto3
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource

from models.short_url import ShortUrlModel
from models.short_url_group import ShortUrlGroupModel
from utils.hash_string import hash_string
from utils.generate_random_string import generate_random_string
from main import short_id_length


class ShortUrlAlreadyExistsException(Exception):
	pass


class Db:
	_session: boto3.Session
	_dynamodb: DynamoDBServiceResource
	_short_url_group_id_length: int = 8

	def __init__(self) -> None:
		Exception('Do not instantiate this class')
		return

	@staticmethod
	def setup():

		# Initialize a session using Amazon DynamoDB
		# it should pull access id and key from environment
		# variables
		Db._session = boto3.Session(
			# aws_access_key_id='YOUR_ACCESS_KEY',
			# aws_secret_access_key='YOUR_SECRET_KEY',
			region_name="us-east-1"
		)
		Db._dynamodb = session.resource("dynamodb")  # type: ignore
		return

	@staticmethod
	async def get_urls() -> list[ShortUrlModel]:
		return []

	@staticmethod
	async def get_original_url(short_url_id: str) -> ShortUrlModel:
		return ShortUrlModel()

	@staticmethod
	async def create_short_url(
		original_url: str,
		short_url_id: str | None,
	):
		"""
		Returns the id of the short url, not the full
		short url since that depends on domain and scheme
		"""
		if short_url_id != None:
			return Db._create_short_url_custom_id(original_url, short_url_id)

		while True:
			short_url_id = generate_random_string(short_id_length)
			group_id: str = hash_string(
				short_url_id, Db._short_url_group_id_length)
			group: ShortUrlGroupModel | None = await Db._get_url_group(group_id)
			if group == None:
				group = ShortUrlGroupModel()
			if not group.contains_short_url_id(short_url_id):
				break
		group.url_pairs.append(
			ShortUrlModel(
				id=short_url_id,
				original_url=original_url,
			)
		)
		group.save()
		return short_url_id

	@staticmethod
	async def _create_short_url_custom_id(
		original_url: str,
		short_url_id: str,
	):
		group_id: str = hash_string(
			short_url_id, Db._short_url_group_id_length)
		group: ShortUrlGroupModel | None = await Db._get_url_group(group_id)
		if group == None:
			group = ShortUrlGroupModel()
		if group.contains_short_url_id(short_url_id):
			raise ShortUrlAlreadyExistsException()

		group.url_pairs.append(
			ShortUrlModel(
				id=short_url_id,
				original_url=original_url,
			)
		)
		group.save()
		return short_url_id

	@staticmethod
	async def _get_url_group(url_group_id: str) -> ShortUrlGroupModel | None:
		"""
		Returns either the group associated with the group id
		or None if it doesn't exist
		"""
		return ShortUrlGroupModel()

	@staticmethod
	def _table_exists(table_name: str) -> bool:
		try:
			Db._dynamodb.meta.client.describe_table(TableName=table_name)
			return True
		except ClientError:
			return False

	@staticmethod
	def _create_table(table_name: str) -> bool:
		if Db._table_exists(table_name):
			raise Exception("table already exists")

		try:
			table = Db._dynamodb.create_table(
				TableName=table_name,
				# Partition key
				KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
				AttributeDefinitions=[
					{"AttributeName": "id", "AttributeType": "S"}],
				ProvisionedThroughput={
					"ReadCapacityUnits": 10,
					"WriteCapacityUnits": 10,
				},
			)
			table.wait_until_exists()
			return True
		except ClientError:
			return False

	# Put an item in the table
	@staticmethod
	def put_item(table_name: str, item) -> bool:  # type: ignore
		table = Db._dynamodb.Table(table_name)
		try:
			table.put_item(Item=item)  # type: ignore
			return True
		except ClientError:
			return False

	# Get an item from the table
	@staticmethod
	def get_item(table_name: str, key: str):
		table = Db._dynamodb.Table(table_name)
		try:
			# presumes that the partition key is in the
			# format of 'id': [str]
			response = table.get_item(Key={"id": key})
			item = response.get("Item")
			return item
		except ClientError:
			return None

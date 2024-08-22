from typing import Any, Dict, List
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource


class PynamoDB:
	_session: boto3.Session | None = None
	_dynamodb: DynamoDBServiceResource | None = None

	def __init__(self) -> None:
		Exception('Do not instantiate this class')
		return

	@classmethod
	def open_connection(cls):
		"""
		Initialize a session using Amazon DynamoDB
		it should pull access id and key from environment
		variables
		"""
		cls._session = boto3.Session(
			region_name="us-east-1"
		)
		cls._dynamodb = cls._session.resource("dynamodb") # type: ignore
		if cls._session is None or cls._dynamodb is None: # type: ignore
			raise Exception('Failed to connect database')
		return
	
	@classmethod
	def close_connection(cls):
		cls._session = None
		cls._dynamodb = None
		print('pynamo reset')
		return

	@classmethod
	def _put_item(cls, table_name: str, item: Dict[str, Any]) -> bool:
		"""
		Puts an item in the given table or updates the item.
		"""
		if cls._dynamodb is None:
			raise Exception('Database not connected')
		table = cls._dynamodb.Table(table_name)
		try:
			table.put_item(Item=item)
			return True
		except ClientError as e:
			print(e)
			return False

	# Get an item from the table
	@classmethod
	def _get_item(cls, table_name: str, key: str) -> Dict[str, Any] | None:
		"""
		Gets an item from the given table if present.
		"""
		if cls._dynamodb is None:
			raise Exception('Database not connected')
		table = cls._dynamodb.Table(table_name)
		try:
			# presumes that the partition key is in the
			# format of 'id': str
			response = table.get_item(Key={'id': key})
			if 'Item' not in response: return None
			return response['Item']
		except ClientError as e:
			print(e)
			return None
	
	@classmethod
	def _scan_table(cls, table_name: str) -> List[Dict[str, Any]]:
		"""
		Gets all items from the given table.
		"""
		if cls._dynamodb is None:
			raise Exception('Database not connected')
		table = cls._dynamodb.Table(table_name)

		response = table.scan()
		items = response.get('Items', [])

		# Handle pagination
		while 'LastEvaluatedKey' in response:
			response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
			items.extend(response.get('Items', []))

		return items
	
	@classmethod
	def _create_table(
		cls,
		table_name: str,
		read_capacity: int = 10,
		write_capacity: int = 10,
		) -> bool:
		if cls._dynamodb is None:
			raise Exception('Database not connected')
			# check if the table already exists
		try:
			cls._dynamodb.Table(table_name).load()
			return True
		except:
			# if it doesn't exist, an error will throw
			# then, create the table
			pass
		try:
			table = cls._dynamodb.create_table(
				TableName=table_name,
				KeySchema=[
					{
						'AttributeName': 'id',
						'KeyType': 'HASH'
					}
				],
				AttributeDefinitions=[
					{
						'AttributeName': 'id',
						'AttributeType': 'S'
					}
				],
				ProvisionedThroughput={
					'ReadCapacityUnits': read_capacity,
					'WriteCapacityUnits': write_capacity,
				}
			)
			table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
			return True
		except Exception as e:
			print(f'Failed to create table: {e}')
			return False

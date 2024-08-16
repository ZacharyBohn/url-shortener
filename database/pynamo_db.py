from typing import Any, Dict, List
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource


class PynamoDB:
	_session: boto3.Session
	_dynamodb: DynamoDBServiceResource

	def __init__(self) -> None:
		Exception('Do not instantiate this class')
		return

	@staticmethod
	def setup():
		"""
		Initialize a session using Amazon DynamoDB
		it should pull access id and key from environment
		variables
		"""
		PynamoDB._session = boto3.Session(
			region_name="us-east-1"
		)
		PynamoDB._dynamodb = PynamoDB._session.resource("dynamodb") # type: ignore
		return

	@staticmethod
	def _put_item(table_name: str, item: Dict[str, Any]) -> bool:
		"""
		Puts an item in the given table or updates the item.
		"""
		table = PynamoDB._dynamodb.Table(table_name)
		try:
			table.put_item(Item=item)
			return True
		except ClientError as e:
			print(e)
			return False

	# Get an item from the table
	@staticmethod
	def _get_item(table_name: str, key: str) -> Dict[str, Any] | None:
		"""
		Gets an item from the given table if present.
		"""
		table = PynamoDB._dynamodb.Table(table_name)
		try:
			# presumes that the partition key is in the
			# format of 'id': str
			response = table.get_item(Key={'id': key})
			if 'Item' not in response: return None
			return response['Item']
		except ClientError as e:
			print(e)
			return None
	
	@staticmethod
	def _scan_table(table_name: str) -> List[Dict[str, Any]]:
		"""
		Gets all items from the given table.
		"""
		table = PynamoDB._dynamodb.Table(table_name)

		response = table.scan()
		items = response.get('Items', [])

		# Handle pagination
		while 'LastEvaluatedKey' in response:
			response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
			items.extend(response.get('Items', []))

		return items

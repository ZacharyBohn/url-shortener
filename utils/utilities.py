import hashlib
from uuid import uuid4
from pydantic import PositiveInt

from ..interfaces.utilities import IUtilities


class Utilities(IUtilities):
	def generate_random_string(self, length: int) -> str:
		if length < 1:
			return ''
		return str(uuid4())[:length]

	def hash_string(self, string: str, output_length: PositiveInt) -> str:
		hash_bytes: bytes = hashlib.sha256(string.encode()).digest()
		hex_encoded: str = hash_bytes.hex()[:output_length]
		return hex_encoded
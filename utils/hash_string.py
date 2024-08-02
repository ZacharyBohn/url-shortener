import hashlib
from pydantic import PositiveInt

def hash_string(string: str, output_length: PositiveInt) -> str:
  hash_bytes: bytes = hashlib.sha256(string.encode()).digest()
  hex_encoded: str = hash_bytes.hex()[:output_length]
  return hex_encoded
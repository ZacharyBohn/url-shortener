import re
from enum import Enum
import hashlib

class InvalidUrlException(Exception): pass

class UrlScheme(Enum):
    HTTP = "http"
    HTTPS = "https"

def generate_short_url(
  url: str,
  short_id_length: int,
  scheme: UrlScheme,
  domain_name: str,
  ) -> str:
  """Generates a short url given a real url
  
  Args:
    url: the real URL that a short url will be generated for
    short_id_length: how long the short url id will be
    scheme: used to specify either http or https
    domain_name: the domain name of this service. This is be
      the domain name of the generated short url
  
  Returns:
    A short url generated using the given url
  
  Raises:
    InvalidUrlException: if the given url is not in a valid format
  """
  if not is_valid_url(url):
    raise InvalidUrlException()
  random_sequence: str = hash_url(url, short_id_length)
  return f"{scheme.value}://{domain_name}/{random_sequence}"

def is_valid_url(url: str) -> bool:
    valid_url_expression: str = r''
    # valid scheme
    valid_url_expression += r"^(" + "|".join(scheme.value for scheme in UrlScheme) + ")://"
    # domain
    valid_url_expression += r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
    # or localhost
    valid_url_expression += r"localhost|"
    # or IP address
    valid_url_expression += r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    # optional port number
    valid_url_expression += r"(?::\d+)?"
    # path after domain
    valid_url_expression += r"(?:/?|[/?]\S+)$"
      
    url_pattern = re.compile(
        valid_url_expression,
        re.IGNORECASE
    )

    return url_pattern.match(url) != None

def hash_url(url: str, output_length: int) -> str:
  hash_bytes: bytes = hashlib.sha256(url.encode()).digest()
  hex_encoded: str = hash_bytes.hex()[:output_length]
  return hex_encoded
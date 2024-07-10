import random
import string
import re
from enum import Enum

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
  """Generates a short url or raises InvalidUrlException"""
  if not is_valid_url(url):
    raise InvalidUrlException()
  random_sequence: str = get_random_alphanumerical(short_id_length)
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

def get_random_alphanumerical(length: int) -> str:
  characters = list(string.ascii_letters) + [str(x) for x in range(0, 10)]
  alphanumerical_sequence = ''
  for _ in range(length):
    r: str = random.choice(characters)
    alphanumerical_sequence += r
  return alphanumerical_sequence
import random
import string

def generate_random_string(length: int):
	if length < 1:
		return ''
	# alphanumeric, both upper and lower case
	characters = string.ascii_letters + string.digits
	random_string = ''.join(random.choice(characters) for _ in range(length))
	return random_string
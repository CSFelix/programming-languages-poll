import uuid

def generate_key():
	"""Generates a random uuid in format HEXADECIMAL and converts it to STRING"""
	return str(uuid.uuid4())
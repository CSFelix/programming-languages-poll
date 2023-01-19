import os
from deta import Deta # pip install deta
from dotenv import load_dotenv # pip install python-dotenv



# ---- LOADING ENVIRONMENT VARIABLES ----
load_dotenv('.env')
DETA_KEY = os.getenv('DETA_KEY')



# ---- INITIALIZING DETA PROJECT AND CONNECTING TO THE DATABASE ----
deta = Deta(DETA_KEY)
db = deta.Base('programming_languages_poll_db')



# ---- FUNCTIONS ----
def insert_answer(key, name, email, age, region
	, programming_area, programming_languages
	, fav_programming_language, years_experience
	, fav_color):
	
	"""
	Returns the poll answers on a successfull answer creation,
	otherwise reises an error.
	"""
	return db.put({
		'key': key, 'name': name, 'email': email, 'age': age, 'region': region
		, 'programming_area': programming_area, 'programming_languages': programming_languages
		, 'fav_programming_language': fav_programming_language, 'years_experience': years_experience
		, 'fav_color': fav_color
	})



def fetch_all_answers():
	"""Returns a dict of all answers"""
	response = db.fetch()
	return response.items # available attributes: 'items', 'last', 'count'



def count_answers():
	"""Returns the number of answers"""
	response = db.fetch()
	return response.count
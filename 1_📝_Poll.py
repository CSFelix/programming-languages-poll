import os
from pathlib import Path
import re

import pandas as pd # pip install pandas

import streamlit as st # pip install streamlit
from streamlit_extras.colored_header import colored_header # pip install streamlit-extras
from streamlit_extras.metric_cards import style_metric_cards # pip install streamlit-extras

import plotly.express as px # pip install plotly

import assets.database as db
import assets.key_generator as kg

# ---- PATH SETTINGS ----
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
css_file = current_dir / 'css' /'main.css'



# ---- VARIABLES ----
PAGE_TITLE = 'Programming Languages Poll'
PAGE_ICON = ':bar_chart:'
PAGE_DESCRIPTION = 'Are you a programmer? So answer the poll!!'
LAYOUT = 'wide'
SIDEBAR_INITIAL_STATE = 'collapsed' # 'auto', 'expanded', 'collapsed'

EMAIL = 'csfelix08@gmail.com'
SOCIAL_MEDIAS = {
	'GitHub': 'https://github.com/csfelix'
	, 'Kaggle': 'https://www.kaggle.com/dsfelix'
	, 'Portfolio': 'https://csfelix.github.io'
	, 'LinkedIn': 'https://linkedin.com/in/csfelix'
}



# ---- PAGE SETTINGS ----
st.set_page_config(
	page_title=PAGE_TITLE
	, page_icon=PAGE_ICON
	, layout=LAYOUT
	, initial_sidebar_state=SIDEBAR_INITIAL_STATE
)




# ---- LAODING CSS FILE ---
with open(css_file) as f:
	st.markdown(f'<style>{ f.read() }</style>', unsafe_allow_html=True)



# ---- SIDEBAR ----
with st.sidebar:
	# Social Medias
	st.header('🤳 Social Medias')
	st.markdown('#')

	cols = st.columns(len(SOCIAL_MEDIAS))
	for index, (platform, link) in enumerate(SOCIAL_MEDIAS.items()):
		cols[index].write(f'[{platform}]({link})')

	st.markdown('----')

	# E-mail
	st.header('📧 Hit me up by E-Mail')
	st.markdown('#')
	contact_form = f"""
	<form action="https://formsubmit.co/{EMAIL}" method="POST">
		<input class="contact_form_input" type="hidden" name="_captcha" value="false" />
		<input class="contact_form_input" type="text" name="name" placeholder="Your Name" required />
		<input class="contact_form_input" type="email" name="email" placeholder="Your Email" required />
		<textarea class="contact_form_input" name="message" placeholder="Your Message Here..." required></textarea>
		<button type"submit" class="button">Send!</button>
	</form>
	"""
	st.markdown(contact_form, unsafe_allow_html=True)



# ---- PAGE TITLE ----
colored_header(
	label=f'{PAGE_ICON} {PAGE_TITLE}'
	, description=PAGE_DESCRIPTION
	, color_name='violet-70'
)
st.markdown('#')



# ---- POLL ----

# Lists
regions_list = ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Australia', 'Antarctica']
programming_area_list = ['Student', 'Data Scientist', 'Full-Stack Developer', 'Mobile Developer', 'Web Developer', 'Designer', 'Security', 'Back-End Developer', 'Front-End Developer', 'Database Manager', 'Business Inteligence', 'Manager', 'Other']
programming_languages_list = ['Python', 'R', 'Scala', 'Julia', 'Elixir', 'JavaScript', 'NodeJS', 'Java', 'C', 'C#', 'C++', 'PHP', 'Pearl', 'Ruby', 'Ruby on Trails', 'Kotlin', 'Swift', 'Go', 'Lua', 'Hack', 'Pascal', 'Assembly', 'Rust', 'SQL']
years_experience_list = ['Under 3 months', '3 months to 1 year', '1 year to 5 years', '5 years to 10 years', '10+ years']
colors_list = ['Purple', 'Blue', 'Yellow', 'Red', 'Green', 'Orange', 'Brown', 'White', 'Gray', 'Black', 'Pink', 'Silver']

# Personal Info
st.info(body='Personal Info', icon='📛')
st.markdown('##')
name = st.text_input(label='Your Name:', placeholder='Felix')
email = st.text_input(label='Your Email:', placeholder='felix@felix.com')
age = st.number_input(label='Your Age:', min_value=8, max_value=100)
region = st.selectbox(label='Your Region:', options=regions_list, index=0, help='Select the continent you are current living')

st.markdown('----')

# Programming Info
st.info(body='Programming Info', icon='💻')
st.markdown('##')
programming_area = st.selectbox(label='Programming Area:', options=programming_area_list, index=0, help='If you have worked in more than one area, select your current one.\nIf you are still a student, select the "Student" option')
programming_languages = st.multiselect(label='Programming Languages Known:', options=programming_languages_list, default=programming_languages_list[0:2])
fav_programming_language = st.selectbox(label='Favorite Programming Language:', options=programming_languages, index=0)
years_experience = st.selectbox(label='Years of Experience:', options=years_experience_list, index=0)

st.markdown('----')

# Random Info
st.info(body='Random Info', icon='🎨')
st.markdown('##')
fav_color = st.selectbox(label='Favorite Color:', options=colors_list, index=0)

st.markdown('#')

# Submit Button
submit_button = st.button(label='Submit!', type='primary')



# ---- POLL SUBMISSION ----
if submit_button:
	fields_flag = name != '' and email != '' and age != '' and region != ''      \
		          and programming_area != '' and programming_languages != ''     \
		          and fav_programming_language != '' and years_experience != ''  \
		          and fav_color != ''
	email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	email_flag = re.fullmatch(email_pattern, email)

	# if all fields are filled and the e-mail follows its pattern
	# the datas are stored into the database hosted on Deta
	if fields_flag and email_flag:
		# application tries to store the answer into the database		
		try:
			db.insert_answer(kg.generate_key(), name, email, age, region, programming_area, programming_languages, fav_programming_language, years_experience, fav_color)
		
		# if an error occur to save the answer, a message is displayed			
		except Exception as error:
			st.markdown('----')
			st.error(
				f"""
				😥 An error occured while saving your answer. Try again after a few minutes!\n
				The error: {error}
				"""
			)

		# if the answer has been succecssfully inserted, the dashboard
		# button is displayed
		else:
			st.markdown('----')
			st.success('🎉 Your answer has been successfully submitted!! Expand the vertical menu on the top-left side and tap on Dashboard page')


	# if some fields are empty, a warning is displayed
	elif not fields_flag:
		st.markdown('----')
		st.warning('🤔 Uh-oh, it looks like you forgot to fill all the fields!')

	# if the informed e-mail does not follow the e-mail pattern,
	# a warning is displayed
	elif not email_flag:
		st.markdown('----')
		st.warning('🤔 Uh-oh, it looks like the informed e-mail is invalid. Check it out and try again!')
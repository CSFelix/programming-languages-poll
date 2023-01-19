import pandas as pd # pip install pandas

import streamlit as st # pip install streamlit
from streamlit_extras.colored_header import colored_header # pip install streamlit-extras
from streamlit_extras.metric_cards import style_metric_cards # pip install streamlit-extras

import plotly.express as px # pip install plotly

import assets.database as db

# ---- PATH SETTINGS ----
css_file = 'css/main.css'



# ---- VARIABLES ----
PAGE_TITLE = 'Programming Languages Poll'
PAGE_ICON = ':bar_chart:'
PAGE_DESCRIPTION = 'Here are the Poll Results!'
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



# ---- GETTING ALL ANSWERS FROM THE DATABASE ----
answers = db.fetch_all_answers()
number_answers = db.count_answers()



# ---- LISTS ----
years_dict = {'Under 10 years': 0, '10 - 19 years': 0, '20 - 29 years': 0, '30 - 39 years': 0, '40+ years': 0}
regions_dict = {'North America': 0, 'South America': 0, 'Europe': 0, 'Africa': 0, 'Asia': 0, 'Australia': 0, 'Antarctica': 0}
programming_area_dict = {'Student': 0, 'Data Scientist': 0, 'Full-Stack Developer': 0, 'Mobile Developer': 0, 'Web Developer': 0, 'Designer': 0, 'Security': 0, 'Back-End Developer': 0, 'Front-End Developer': 0, 'Database Manager': 0, 'Business Inteligence': 0, 'Manager': 0, 'Other': 0}
programming_languages_dict = {'Python': 0, 'R': 0, 'Scala': 0, 'Julia': 0, 'Elixir': 0, 'JavaScript': 0, 'NodeJS': 0, 'Java': 0, 'C': 0, 'C#': 0, 'C++': 0, 'PHP': 0, 'Pearl': 0, 'Ruby': 0, 'Ruby on Trails': 0, 'Kotlin': 0, 'Swift': 0, 'Go': 0, 'Lua': 0, 'Hack': 0, 'Pascal': 0, 'Assembly': 0, 'Rust': 0, 'SQL': 0}
fav_programming_languages_dict = {'Python': 0, 'R': 0, 'Scala': 0, 'Julia': 0, 'Elixir': 0, 'JavaScript': 0, 'NodeJS': 0, 'Java': 0, 'C': 0, 'C#': 0, 'C++': 0, 'PHP': 0, 'Pearl': 0, 'Ruby': 0, 'Ruby on Trails': 0, 'Kotlin': 0, 'Swift': 0, 'Go': 0, 'Lua': 0, 'Hack': 0, 'Pascal': 0, 'Assembly': 0, 'Rust': 0, 'SQL': 0}
years_experience_dict = {'Under 3 months': 0, '3 months to 1 year': 0, '1 year to 5 years': 0, '5 years to 10 years': 0, '10+ years': 0}
fav_colors_dict = {'Purple': 0, 'Blue': 0, 'Yellow': 0, 'Red': 0, 'Green': 0, 'Orange': 0, 'Brown': 0, 'White': 0, 'Gray': 0, 'Black': 0, 'Pink': 0, 'Silver': 0}



# ---- PROCESSING THE ANSWERS ----

# Dropping 'name', 'email' and 'key' attributes
for index in range(len(answers)):
	answers[index].pop('name')
	answers[index].pop('key')
	answers[index].pop('email')



# Updating dictionaries
for answer in answers:

	# Age
	age = answer['age']
	if age < 10: years_dict['Under 10 years'] += 1
	elif age >= 10 and age < 20: years_dict['10 - 19 years'] += 1
	elif age >= 20 and age < 30: years_dict['20 - 29 years'] += 1
	elif age >= 30 and age < 40: years_dict['30 - 39 years'] += 1
	else: years_dict['40+ years'] += 1


	# Regions and Programming Area
	regions_dict[answer['region']] += 1
	programming_area_dict[answer['programming_area']] += 1

	# Programming Languages
	for language in answer['programming_languages']: programming_languages_dict[language] += 1

	# Fav Programming Language, Years of Experience and Fav Colors
	fav_programming_languages_dict[answer['fav_programming_language']] += 1
	years_experience_dict[answer['years_experience']] += 1
	fav_colors_dict[answer['fav_color']] += 1



# ---- PLOTS ----
years_df = pd.DataFrame({'Years': years_dict.keys(), 'Count': years_dict.values()})
regions_df = pd.DataFrame({'Regions': regions_dict.keys(), 'Count': regions_dict.values()})
programming_area_df = pd.DataFrame({'Areas': programming_area_dict.keys(), 'Count': programming_area_dict.values()}).sort_values(by='Count', ascending=False).head()
programming_languages_df = pd.DataFrame({'Languages': programming_languages_dict.keys(), 'Count': programming_languages_dict.values()}).sort_values(by='Count', ascending=False).head()
fav_programming_languages_df = pd.DataFrame({'Languages': fav_programming_languages_dict.keys(), 'Count': fav_programming_languages_dict.values()}).sort_values(by='Count', ascending=False).head()
years_experience_df = pd.DataFrame({'Years': years_experience_dict.keys(), 'Count': years_experience_dict.values()})
fav_colors_df = pd.DataFrame({'Colors': fav_colors_dict.keys(), 'Count': fav_colors_dict.values()}).sort_values(by='Count', ascending=False).head()

years_plot = px.bar(years_df, x='Years', y='Count', title='Programmers Years-Old Distribution')
regions_plot = px.bar(regions_df, x='Regions', y='Count', title='Continents Distribution')
programming_area_plot = px.bar(programming_area_df, x='Areas', y='Count', title='Top 5 Areas')
programming_languages_plot = px.bar(programming_languages_df, x='Languages', y='Count', title='Top 5 Known Programming Languages')
fav_programming_languages_plot = px.bar(fav_programming_languages_df, x='Languages', y='Count', title='Top 5 Favorite Programming Languages')
years_experience_plot = px.bar(years_experience_df, x='Years', y='Count', title='Years of Experience Distribution')
fav_colors_plot = px.bar(fav_colors_df, x='Colors', y='Count', title='Top 5 Favorite Colors')



# ---- PLOTTING ----

st.plotly_chart(years_plot, use_container_width=True)
st.markdown('----')

st.plotly_chart(regions_plot, use_container_width=True)
st.markdown('----')

st.plotly_chart(programming_area_plot, use_container_width=True)
st.markdown('----')

st.plotly_chart(programming_languages_plot, use_container_width=True)
st.markdown('----')

st.plotly_chart(fav_programming_languages_plot, use_container_width=True)
st.markdown('----')

st.plotly_chart(years_experience_plot, use_container_width=True)
st.markdown('----')

st.plotly_chart(fav_colors_plot, use_container_width=True)
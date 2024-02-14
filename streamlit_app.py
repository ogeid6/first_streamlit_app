import streamlit
import pandas as pd
import requests
import snowflake.connector
import urllib.error


# menu  
streamlit.title("Breakfast Favorites")
streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# macros table
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


# fruityvice advice
streamlit.header("Fruityvice fruit advice")
def fruityvice_data(fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return streamlit.dataframe(fruityvice_normalized)
try:
  fruit_choice = streamlit.text_input('what fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please select a fruit to get information")
  else:
    fruityvice_data(fruit_choice)
except URLError as e:
  streamlit.error()

# get fruit list from snowflake
streamlit.header("the fruit load list contains:")
def get_fruit_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    my_data_row = my_cur.fetchall()
    return streamlit.dataframe(my_data_row)
if streamlit.button('Get fruit list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  get_fruit_list()
  

# adding fruit to the list
add_my_fruit = streamlit.text_input('what fruit would you like to load?')
if streamlit.button('add fruit to the list'):
  my_cur.execute("insert into FRUIT_LOAD_LIST values ('" + add_my_fruit + "')")
  streamlit.text = ('Thanks for adding', add_my_fruit)
  

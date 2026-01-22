# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import snowflake.connector
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie! 
  """
)

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smothiee will be', name_on_order)

option = st.selectbox(('How would you like to be contacted?'), 
                      ('Email', 'Home Phone', 'Mobile phone'), index = None)
st.write('You selected', option)
#fruit = st.selectbox(('What is your favourite fruit?'), 
                      #('Banana', 'Starawberries', 'Peaches'), index = None)
#st.write('Your favourite fruis is ', fruit)

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingridient_list = st.multiselect('Chooce fruits which u like: ', my_dataframe, max_selections = 5 )
if ingridient_list:
    #st.write(ingridient_list)
    #st.text(ingridient_list)
    ingredients_string = ''
    for fruit_chosen in ingridient_list:
        ingredients_string +=fruit_chosen + ' '
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import snowflake.connector
import requests
import pandas as pd


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

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col('SEARCH_ON'))
#st.stop()                                                                      
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)


ingridient_list = st.multiselect('Chooce fruits which u like: ', my_dataframe, max_selections = 5 )
if ingridient_list:
    #st.write(ingridient_list)
    #st.text(ingridient_list)
    ingredients_string = ''
  
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
  
    for fruit_chosen in ingridient_list:
        ingredients_string +=fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition info: ')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


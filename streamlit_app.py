# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize your Smoothie")
st.write("Please enter your name below")

title = st.text_input("Name")
st.write("Name : ", title)



cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()                                                                      

st.write("Customize your smoothie by selecting fruits from below options")
ingredients_list =st.multiselect('Choose upto 5', my_dataframe, max_selections = 5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients = ''

    for x in ingredients_list:
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == x, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', x,' is ', search_on, '.')
        st.subheader(x +' Fruit Nutritients')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+x)
        fv_df= st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        ingredients +=x +' ' 

    #st.write(ingredients)

    but = st.button('Submit')

    if but:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients + """', '"""+ title +"""')"""

        #st.write(my_insert_stmt)

        if ingredients:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
            




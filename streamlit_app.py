# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize your Smoothie")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

title = st.text_input("Smoothie name")
st.write("Name : ", title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list =st.multiselect('Choose upto 5', my_dataframe, max_selections = 5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients = ''

    for x in ingredients_list:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
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
            




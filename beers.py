
import streamlit as st
import pandas as pd
import numpy as np


# Define your custom CSS
background_css = """
<style>
    .stApp {
        #background-image: url('https://balticfresh.com/image/cache/catalog/Products/383L-min-800x800.jpg');
	background-image: url('https://beerplanet.net/wp-content/uploads/2017/03/Lager.jpg');
       	background-size: 300px;
        background-position: left;
        background-repeat: no-repeat;
    }
</style>
"""

# Inject the custom CSS into the Streamlit app
st.markdown(background_css, unsafe_allow_html=True)


st.title("Worldwide Beer Superstore")


DATA_URL = ('https://raw.githubusercontent.com/Declantn/uber/main/beermap.csv')

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


data = load_data()
data.set_index('beer_beerid', inplace=True)

# read in the output of the item/item reccomender script - Top 5 beers to be reccomended based on choice
top5 = pd.read_csv("https://raw.githubusercontent.com/Declantn/uber/main/top5beers.csv")
top5.set_index('beer_beerid', inplace=True)







#drop all values where we do not have co-ordinates
with_ll = data.dropna(subset=['lat'])
st.subheader('Beers from countries across the globe' )
st.map(with_ll)



unique_country = data["country_name"].unique()

# Create a select box
selected_country = st.selectbox('**Select an country:**', unique_country)



filtered_df = data[data["country_name"] == selected_country]

unique_style = filtered_df["beer_style"].unique()

# Create a select box
selected_option = st.selectbox('**Select a beer type:**', unique_style)


#reduced the dataset based on beer type
filtered_df = filtered_df[filtered_df["beer_style"] == selected_option]


# Some number in the range 0-10
abv_to_filter = st.slider('**Minimum beer strength**', 0, 10, 3)
abv_selected = filtered_df[filtered_df["beer_abv"] >= abv_to_filter]

# Select an average beer rating
rating_filter = st.slider('**User rating score**', 0, 5, 3)
selected_beers = abv_selected[abv_selected["review_overall"] >= rating_filter]

#only display relevent columns
selected_beers_disp = selected_beers[["brewery_name","beer_name","beer_abv","mean_review_overall"]]
selected_beers_disp.reset_index(drop=True, inplace=True)

st.write('**Beers which match your criteria**')

selected_beers_disp = selected_beers_disp.rename(columns={'brewery_name': 'Brewery','beer_name': "Beer","beer_abv": "Strength", "mean_review_overall":"User rating"})
st.dataframe(selected_beers_disp, use_container_width=True)

# Create a selectbox for users to select a beer by name
beer_options = selected_beers['beer_name'].tolist()
selected_beer = st.selectbox('**Select which beer to add to your basket**:', beer_options)

selected_beer_id = selected_beers.index[selected_beers['beer_name'] == selected_beer]



#find the reccomended beers based on the users choice
rec_beers = top5.loc[selected_beer_id]
rec_beers_t5 = rec_beers.iloc[:, 0:5]

# Display the selected option
#st.write('Rec Beers Top:', rec_beers_t5)

rec_beers_t5_flat = rec_beers_t5.values.ravel()

# Select rows from data based on the values in rec_beers_t5_flat

selected_rows = data[data.index.isin(rec_beers_t5_flat)]


selected_rows = selected_rows.reset_index(drop=True)

st.write("**Beers we reccomend you try**")

Rec_beers_disp = selected_rows[["country_name","beer_style","brewery_name","beer_name"]]
Rec_beers_disp = Rec_beers_disp.rename(columns={'brewery_name': 'Brewery','beer_name': "Beer","beer_style": "Beer Type", "country_name":"Country"})
st.dataframe(Rec_beers_disp.iloc[:, 0:], use_container_width=True)




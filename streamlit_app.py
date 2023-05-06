from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import psycopg2
import time
import folium
from streamlit_folium import st_folium, folium_static


@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

conn = init_connection()

#map from existing data
rows = run_query("SELECT location, lat, lon, average_measure, number_of_measures FROM public.openaq_agg;")
df = pd.DataFrame(rows, columns=['location', 'lat', 'lon', 'average_measure', 'number_of_measures'])
m = folium.Map(location=[df.lat.mean(), df.lon.mean()], zoom_start=3, control_scale=True)

for i, row in df.iterrows():
    # Setup the content of the popup
    iframe = folium.IFrame('location:' + str(row["location"]))

    # Initialise the popup using the iframe
    popup = folium.Popup(iframe, min_width=300, max_width=300)

    # Add each row to the map
    folium.Marker(location=[row['lat'], row['lon']],
                  popup=popup, c=row['location']).add_to(m)

    st_data = st_folium(m, width=700)


placeholder = st.empty()

while 1 == 1:
    with placeholder.container():

        rows = run_query("SELECT location, lat, lon, average_measure, number_of_measures FROM public.openaq_agg;")
        df = pd.DataFrame(rows, columns=['location', 'lat', 'lon', 'average_measure', 'number_of_measures'])
        st.dataframe(df, width=700)

        time.sleep(5)

# for row in rows:
#    st.write(f"{row[0]} has a :{row[1]}:")

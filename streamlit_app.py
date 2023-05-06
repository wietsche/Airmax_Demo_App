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
#

conn = init_connection()
#
## Perform query.
## Uses st.cache_data to only rerun when the query changes or after 10 min.

placeholder = st.empty()
#m = folium.Map(location=[df.lat.mean(), df.lon.mean()], zoom_start=3, control_scale=True)
m = folium.Map(control_scale=True)


while 1 == 1:
    with placeholder.container():

        #@st.cache_data(ttl=1)
        def run_query(query):
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

        rows = run_query("SELECT location, lat, lon, average_measure, number_of_measures FROM public.openaq_agg;")
        df = pd.DataFrame(rows, columns =['location', 'lat', 'lon', 'average_measure','number_of_measures'])
        st.dataframe(df)

        fg = folium.FeatureGroup(name="measures")

        for i, row in df.iterrows():
            # Setup the content of the popup
            iframe = folium.IFrame('Measure:' + str(row["average_measure"]))

            # Initialise the popup using the iframe
            popup = folium.Popup(iframe, min_width=300, max_width=300)

            # Add each row to the map
            marker folium.Marker(location=[row['lat'], row['lon']],
                          popup=popup, c=row['average_measure'])
            fg.add_child(m)

        #st_data = st_folium(m, width=700)

        out = st_folium(
            m,
            feature_group=fg,
            center=center,
            width=1200,
            height=500,
        )

        time.sleep(5)
#for row in rows:
#    st.write(f"{row[0]} has a :{row[1]}:")

from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import psycopg2


@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])
#

conn = init_connection()
#
## Perform query.
## Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=1)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT location, lat, lon, average_measure, number_of_measures FROM public.openaq_agg;")
df = pd.DataFrame(rows, columns =['location', 'lat', 'lon', 'average_measure','number_of_measures'])

# Print results.
df = pd.DataFrame()
st.dataframe(df)
#for row in rows:
#    st.write(f"{row[0]} has a :{row[1]}:")


import altair as alt
import pandas as pd
import streamlit as st

data = pd.read_csv("final_mass_data.csv")

url  = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/MA-25-massachusetts-counties.json"

data_map = alt.topo_feature(url, "cb_2015_massachusetts_county_20m")

base = alt.Chart(data_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=600
)

points = alt.Chart(data.iloc[:500,]).mark_circle().encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    size=alt.value(10),
    tooltip='Towns'
)

st.altair_chart(base + points, use_container_width=True)
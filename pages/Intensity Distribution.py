import altair as alt
import pandas as pd
import streamlit as st

# Intensity Map: intensity of PFAs overlayed across the base map of Massachussetts

data = pd.read_csv("final_mass_data.csv")

url  = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/MA-25-massachusetts-counties.json"

data_map = alt.topo_feature(url, "cb_2015_massachusetts_county_20m")

# Intensity Map: intensity of PFAs overlayed across the base map of Massachussetts
base = alt.Chart(data_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=600
)

points = alt.Chart(data).mark_circle().encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    color=alt.Color('Levels', type='quantitative', scale=alt.Scale(scheme='blues', type='log', domain=(0.01,100), reverse=False), legend=alt.Legend(title="Contamination Levels")),
    size=alt.value(30),
    opacity=alt.value(0.1),
    tooltip='Towns'
)

st.altair_chart(base + points, use_container_width=True)
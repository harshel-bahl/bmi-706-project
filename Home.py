import pandas as pd
import altair as alt
import json
import requests
import streamlit as st


data = pd.read_csv("final_mass_data.csv")
url  = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/MA-25-massachusetts-counties.json"

data_map = alt.topo_feature(url, "cb_2015_massachusetts_county_20m")

Map = alt.Chart(data_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=600)

points = alt.Chart(data.iloc[:3000,]).mark_circle(opacity=0.2).encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    #size=alt.Size("Levels:Q",legend=None),
    color = alt.Color("Abbreviation:N",legend=None),
  
    size=alt.value(100),
    tooltip=['Towns','Abbreviation:N'])

Map_chart = Map + points
st.altair_chart(Map_chart, use_container_width=True)
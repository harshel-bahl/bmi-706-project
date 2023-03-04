
import altair as alt
import pandas as pd
import streamlit as st

data = pd.read_csv("final_mass_data.csv")

url  = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/MA-25-massachusetts-counties.json"

data_map = alt.topo_feature("https://raw.githubusercontent.com/harshel-bahl/bmi-706-project/main/MA-25-massachusetts-counties.json?token=GHSAT0AAAAAAB63X2WLDBDXLRR72JL3HEKKZADYCOQ", "cb_2015_massachusetts_county_20m")

print(data_map)

base = alt.Chart(data_map.properties).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=600
)

st.altair_chart(base, use_container_width=True)
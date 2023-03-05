import altair as alt
import pandas as pd
import streamlit as st

# Intensity Map: intensity of PFAs overlayed across the base map of Massachussetts

data = pd.read_csv("final_mass_data.csv")
poss_years = data["Year"].unique()

url  = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/MA-25-massachusetts-counties.json"

data_map = alt.topo_feature(url, "cb_2015_massachusetts_county_20m")

# multi-selector to choose which years to display on chart
selectedYears = st.multiselect("Years Shown", poss_years, poss_years[0])
subData = data[data["Country"].isin(selectedYears)]

# Intensity Map: intensity of PFAs overlayed across the base map of Massachussetts
base = alt.Chart(data_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=600
)

points = alt.Chart(subData).mark_circle().encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    color=alt.Color('Levels', type='quantitative', scale=alt.Scale(scheme='blues', type='log', domain=(0.01,100), reverse=False), legend=alt.Legend(title="Contamination Levels")),
    size=alt.value(30),
    opacity=alt.value(0.1),
    tooltip='Towns'
)

st.altair_chart(base + points, use_container_width=True)
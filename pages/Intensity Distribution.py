import altair as alt
import pandas as pd
import streamlit as st

# Intensity Map: intensity of PFAs overlayed across the base map of Massachussetts

# Pre-processing - get relevant unique values for columns and scale levels
data = pd.read_csv("final_mass_data.csv")
poss_years = data["Year"].unique()

# take json data to create map on streamlit
url  = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/MA-25-massachusetts-counties.json"
data_map = alt.topo_feature(url, "cb_2015_massachusetts_county_20m")

# multi-selector to choose which years to display on chart
selectedYears = st.multiselect("Years Shown", poss_years, poss_years[0], max_selections=3)
subData = data[data["Year"].isin(selectedYears)]
subData["Levels"] = (subData["Levels"]-subData["Levels"].min())/(subData["Levels"].max()-subData["Levels"].min())*100

# Intensity Map: intensity of PFAs overlayed across the base map of Massachussetts
base = alt.Chart(data_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=600
)

levelsScale = alt.Scale(domain=[subData['Levels'].min(), subData['Levels'].max()], scheme='oranges', type='log', clamp=True)
levelsColor = alt.Color(field='Levels', type='quantitative', scale=levelsScale, legend=alt.Legend(title="Contamination Levels"))

points = alt.Chart(subData).mark_circle().encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    color=levelsColor,
    size=alt.value(100),
    opacity=alt.value(1),
    tooltip='Towns'
)

st.altair_chart(base + points, use_container_width=True)
import pandas as pd
import altair as alt
import json
import requests
import geopandas as gpd



data = pd.read_csv("/content/drive/MyDrive/Final Mass Data.csv")
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

base + points
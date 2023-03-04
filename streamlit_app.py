
import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

url  = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/MA-25-massachusetts-counties.json"

data_map = alt.topo_feature(url, "cb_2015_massachusetts_county_20m")

base = alt.Chart(data_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=600
)

import altair as alt
import pandas as pd
import streamlit as st

data = pd.read_csv("final_mass_data.csv")

data_map = alt.topo_feature("MA-25-massachusetts-counties.json", "cb_2015_massachusetts_county_20m")

base = alt.Chart(data_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=600
)

st.altair_chart(base, use_container_width=True)
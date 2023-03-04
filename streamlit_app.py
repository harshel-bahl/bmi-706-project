
import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data


states = alt.topo_feature(data.us_10m.url, feature='states')

alt.Chart(states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('albersUsa').properties(
    width=500,
    height=300
)
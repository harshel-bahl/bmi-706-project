import altair as alt
import pandas as pd
import streamlit as st

# Time Series Chart - show PFA levels over time for a given site

# Pre-processing - get relevant unique values for columns and scale levels
data = pd.read_csv("final_mass_data.csv")
poss_years = data["Year"].unique()
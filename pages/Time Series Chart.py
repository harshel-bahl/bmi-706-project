import altair as alt
import pandas as pd
import streamlit as st

# Time Series Chart - show PFA levels over time for a given site

# Pre-processing - get relevant unique values for columns and scale levels
data1 = pd.read_csv("final_mass_data.csv")

st.write("PFA Levels over time")

siteslist = data1['Site'].unique()
site_select = st.selectbox(label="Site", options=siteslist, index=0)

data = data1[data1["Site"]==site_select]

chemicalslist = data1['Chemical'].unique()

chemicals=st.multiselect(label="Chemical", options = chemicalslist, default = chemicalslist)

data = data[data["Chemical"].isin(chemicals)]

selector = alt.selection_single( fields = ['Chemical'])

base = alt.Chart(data).properties().encode(
    x=alt.X('Date:T'),
    y=alt.Y('Levels:Q'),
    color=alt.Color('Chemical:N')
).add_selection(selector).transform_filter(selector)

brush = alt.selection_interval(encodings=['x'])

upper=base.mark_line(point=True).encode(
    alt.X('Date:T', scale = alt.Scale(domain=brush))
).transform_filter(brush)

lower = base.mark_bar().add_selection(brush)

lower=lower.properties(height=50)

chart1=upper & lower

st.altair_chart(chart1, use_container_width=True)

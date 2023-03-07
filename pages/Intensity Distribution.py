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
selectedYears = st.multiselect("Years Shown", poss_years, default=poss_years[0], max_selections=3)
subData = data[data["Year"].isin(selectedYears)]
subData["Levels"] = (subData["Levels"]-subData["Levels"].min())/(subData["Levels"].max()-subData["Levels"].min())*100

# create contaminant groups for slider
quantiles = [subData["Levels"].quantile(0.9),
             subData["Levels"].quantile(0.8),
             subData["Levels"].quantile(0.7),
             subData["Levels"].quantile(0.6),
             subData["Levels"].quantile(0.5),
             subData["Levels"].quantile(0.4),
             subData["Levels"].quantile(0.3),
             subData["Levels"].quantile(0.2),
             subData["Levels"].quantile(0.1)]

def createGroups(rowValues):
    if rowValues['Levels'] > quantiles[0]:
        return 90
    elif rowValues['Levels'] > quantiles[1] and rowValues['Levels'] < quantiles[0]:
        return 80
    elif rowValues['Levels'] > quantiles[2] and rowValues['Levels'] < quantiles[1]:
        return 70
    elif rowValues['Levels'] > quantiles[3] and rowValues['Levels'] < quantiles[2]:
        return 60
    elif rowValues['Levels'] > quantiles[4] and rowValues['Levels'] < quantiles[3]:
        return 50
    elif rowValues['Levels'] > quantiles[5] and rowValues['Levels'] < quantiles[4]:
        return 40
    elif rowValues['Levels'] > quantiles[6] and rowValues['Levels'] < quantiles[5]:
        return 30
    elif rowValues['Levels'] > quantiles[7] and rowValues['Levels'] < quantiles[6]:
        return 20
    elif rowValues['Levels'] > quantiles[8] and rowValues['Levels'] < quantiles[7]:
        return 10
    elif rowValues['Levels'] < quantiles[8]:
        return 0
    

subData["LevelGroup"] = subData.apply(lambda rowValues: createGroups(rowValues), axis=1)


selectedLevelGroup = st.slider("LevelGroup", min_value=0, max_value=90, step=10, value=50)
subData = subData[subData["LevelGroup"]==selectedLevelGroup]

# Intensity Map: intensity of PFAs overlayed across the base map of Massachussetts
base = alt.Chart(data_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=600
)

# add threshold levels in place of quantiles for interpretability

colorSchemes = ["blues", "oranges", "greens"]

def createChart(inputData, colorScheme):

    levelsScale = alt.Scale(domain=[inputData['Levels'].quantile(0.1), inputData['Levels'].quantile(0.9)], scheme=colorScheme, clamp=True)
    levelsColor = alt.Color(field='Levels', type='quantitative', scale=levelsScale, legend=alt.Legend(title="Contamination Levels"))

    points = alt.Chart(inputData, mark="square").encode(
        longitude='Longitude:Q',
        latitude='Latitude:Q',
        color=levelsColor,
        size=alt.value(100),
        opacity=alt.value(0.5),
        tooltip='Towns'
    )

    return points

chart = base

if len(selectedYears) == 2:
    chart = chart + createChart(subData[subData["Year"]==selectedYears[0]], colorSchemes[0]) #+ createChart(subData[subData["Year"]==selectedYears[1]], colorSchemes[1])

# for i in range(len(selectedYears)):
    
#     chart = chart + createChart(subData["Year"==selectedYears[i]], colorSchemes[i])

st.altair_chart(chart, use_container_width=True)
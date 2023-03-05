import pandas as pd
import altair as alt
import streamlit as st

# Read in the data file
data = pd.read_csv("final_mass_data.csv")

# Read in JSON file to map data
url  = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/MA-25-massachusetts-counties.json"

# Extract Map Data
data_map = alt.topo_feature(url, "cb_2015_massachusetts_county_20m")

# App Aesthetics

# Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Define a dictionary to store the colors of each substance
substance_colors = {
    'PFHPA': 'red', 
    'PFBS': 'green', 
    'PFOA': 'blue', 
    'PFNA': 'orange', 
    'PFOS': 'purple', 
    'PFHXS': 'brown', 
    'PFHXA': 'pink', 
    'PFAS6': 'gray', 
    'NMEFOSAA': 'teal', 
    'PFDA': 'navy', 
    'ADONA': 'olive', 
    'HFPO-DA': 'magenta', 
    '11CL-PF3OUDS': 'maroon', 
    '9CL-PF3ONS': 'coral', 
    'PFUNA': 'indigo', 
    'PFTRDA': 'khaki', 
    'PFTA': 'salmon', 
    'PFDOA': 'sienna'
}


Substance_type = data["Abbreviation"].unique()

# Selection Box for Different Substances
substances = st.multiselect(
    "Types of Per- and Polyfluorinated Substances (PFAS)",
    options = Substance_type,
    default = ["PFOS",
               "PFNA",
               "PFTRDA",
               "ADONA",
               "NMEFOSAA"],
    ##format_func=lambda option: f'<span style="background-color: {substance_colors[option]}; padding: 8px; border-radius: 5px;">{option}</span>'
)

filtered_data = data[data['Abbreviation'].isin(substances)]

# Create a dictionary to map each substance to its corresponding color
substance_color_map = {substance: substance_colors[substance] for substance in filtered_data['Abbreviation'].unique()}


subset = data[data["Abbreviation"].isin(substances)]

year = st.slider(
    "Year",
    min_value = 2016,
    max_value = 2023,
    value = 2019
)
subset = subset[subset["Year"] == year]

Map = alt.Chart(data_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=600)


legend_title = 'Substances'
legend_order = list(substance_color_map.keys())

points = alt.Chart(subset.iloc[:3000,]).mark_circle(opacity=0.1).encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',    
    color=alt.Color("Abbreviation:N", scale=alt.Scale(domain=list(substance_color_map.keys()), range=list(substance_color_map.values()))),
    size=alt.value(600),
    tooltip=['Towns:N','Abbreviation:N'])

Map_chart = Map + points

st.altair_chart(Map_chart, use_container_width=True)



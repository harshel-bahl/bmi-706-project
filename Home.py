import pandas as pd
import altair as alt
import streamlit as st

# Read in the data file
data = pd.read_csv("final_mass_data.csv")

# Read in JSON file to map data
url  = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/MA-25-massachusetts-counties.json"

# Extract Map Data
data_map = alt.topo_feature(url, "cb_2015_massachusetts_county_20m")


# Side bar
st.sidebar.subheader("What are PFAS?")
st.sidebar.info("PFAS (per- and polyfluoroalkyl substances) are a group of synthetic chemicals widely used in various industries and products due to their unique properties.")
st.sidebar.subheader("Potential Problems")           
st.sidebar.info("They are persistent and do not break down easily in the environment, which means they can accumulate in soil, water, and living organisms, including humans, leading to adverse health problems.")
st.sidebar.info("Some PFAS have been associated with adverse health effects, leading to many governments and organizations taking steps to restrict or ban their use and investigate safer alternatives.")


# App Aesthetics

html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">PFAS Water Contamination Monitoring App</h2>
    </div>
    """
st.markdown(html_temp,unsafe_allow_html=True)


st.write("")
st.write("")

# Row A
st.markdown('### Massachusetts PFAS Statistics 2016-2023')
col1, col2, col3 = st.columns(3)
col1.metric("Most Contaminated Town", "HUDSON")
col2.metric("Top PFAS", "PFOS")
col3.metric("Highest Recorded Level", "955 ng/L ")

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
    'ADONA': 'olive', 
    'HFPO-DA': 'magenta', 
    '11CL-PF3OUDS': 'maroon', 
    '9CL-PF3ONS': 'coral', 
    'PFUNA': 'indigo', 
    'PFTRDA': 'khaki',  
    'PFDOA': 'sienna',
    ' PFDA':'black',
    ' PFTA':'white'}


Substance_type = data["Abbreviation"].unique()

st.write("")
st.write("")

# Selection Box for Different Substances
substances = st.multiselect(
    "Select PFAS for Geographic Distribution:",
    options = Substance_type,
    default = ["PFOS"]
)

filtered_data = data[data['Abbreviation'].isin(substances)]

# Create a dictionary to map each substance to its corresponding color
substance_color_map = {substance: substance_colors[substance] for substance in filtered_data['Abbreviation'].unique()}

st.write("")
st.write("")

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



points = alt.Chart(subset).mark_circle(opacity=0.1).encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',    
    color=alt.Color("Abbreviation:N", scale=alt.Scale(domain=list(substance_color_map.keys()), range=list(substance_color_map.values()))),
    size=alt.value(200),   
    tooltip=[alt.Tooltip('Towns:N', title='Location'), alt.Tooltip('Abbreviation:N', title='Substance'),alt.Tooltip('Levels:N', title='Level')])
Map_chart = Map + points

st.altair_chart(Map_chart, use_container_width=True)

# Filter subsetted data based on selected year and substances
subset_filtered = subset.loc[(subset['Year'] == year) & (subset['Abbreviation'].isin(substances)), :]
subset_filtered.Year = subset_filtered.Year.astype(str)

html_temp = """
    <div style="background-color:salmon;padding:10px">
    <h2 style="color:white;text-align:center;">Top PFAS Contaninants by Town</h2>
    </div>
    """
st.markdown(html_temp,unsafe_allow_html=True)

# Show filtered data in a table
st.dataframe(subset_filtered[["Year", "Towns","Abbreviation","Levels"]].sort_values(by="Levels", ascending=False).drop_duplicates(subset="Towns").reset_index(drop=True), width=1000)
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


html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">PFAS Water Contamination Monitoring App</h2>
    </div>
    """
st.markdown(html_temp,unsafe_allow_html=True)


st.write("")
st.write("")

# Row A
st.markdown('### Massachusetts PFAS Statistics')
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
    "Types of Per- and Polyfluorinated Substances (PFAS)",
    options = Substance_type,
    default = ["PFOS",
               "PFNA",
               "PFTRDA",
               "ADONA",
               "NMEFOSAA"]
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


legend_title = 'Substances'
legend_order = list(substance_color_map.keys())

points = alt.Chart(subset.iloc[:3000,]).mark_circle(opacity=0.1).encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',    
    color=alt.Color("Abbreviation:N", scale=alt.Scale(domain=list(substance_color_map.keys()), range=list(substance_color_map.values()))),
    size=alt.value(600),
    #tooltip=['Towns:N','Abbreviation:N'])
    tooltip=[alt.Tooltip('Towns:N', title='Location'), alt.Tooltip('Abbreviation:N', title='Substance')])

Map_chart = Map + points

st.altair_chart(Map_chart, use_container_width=True)

# Filter subsetted data based on selected year and substances
subset_filtered = subset.loc[(subset['Year'] == year) & (subset['Abbreviation'].isin(substances)), :]


html_temp = """
    <div style="background-color:blue;padding:10px">
    <h2 style="color:white;text-align:center;">Top PFAS Contaninants by Town</h2>
    </div>
    """
st.markdown(html_temp,unsafe_allow_html=True)

# Show filtered data in a table
st.dataframe(subset_filtered[["Year", "Towns","Abbreviation","Levels"]].sort_values(by="Levels", ascending=False).drop_duplicates(subset="Towns").reset_index(drop=True), width=1000)
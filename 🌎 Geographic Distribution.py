import pandas as pd
import altair as alt
import streamlit as st

st.set_page_config(page_title="🌎 Geographic Distribution")
# Read in the data file
data = pd.read_csv("final_mass_data.csv")

# Read in JSON file to map data
url  = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/MA-25-massachusetts-counties.json"

# Extract Map Data
data_map = alt.topo_feature(url, "cb_2015_massachusetts_county_20m")

data.Chemical = data.Abbreviation

# Add custom CSS to change the color of the first info box in the sidebar
st.markdown(
    """
    <style>
    .element-container:nth-child(2) .stAlert {
        background-color: #fce5ba;
        color: white;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add custom CSS to change the color of the second info box in the sidebar
st.markdown(
    """
    <style>
    .element-container:nth-child(3) .stAlert {
        background-color: white;
        color: white;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add custom CSS to change the color of the third info box in the sidebar
st.markdown(
    """
    <style>
    .element-container:nth-child(4) .stAlert {
        background-color: white;
        color: black;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .element-container:nth-child(5) .stAlert {
        background-color: #fde6b2;
        color: black;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .element-container:nth-child(6) .stAlert {
        background-color: #fce5ba;
        color: black;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .element-container:nth-child(7) .stAlert {
        background-color: white;
        color: black;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Side bar
st.sidebar.subheader("What are PFAS?")
st.sidebar.info("PFAS (per and polyfluoroalkyl substances) are a group of man-made chemicals that have been used in a variety of industrial and consumer products since the 1950s. They are highly persistent and do not break down easily in the environment or in the human body, earning them the nickname 'forever chemicals.'")
st.sidebar.info("They are persistent and do not break down easily in the environment, which means they can accumulate in soil, water, and living organisms, including humans, leading to adverse health problems.")
st.sidebar.subheader("Potential Health Problems") 
st.sidebar.info("Exposure to PFAS has been linked to a number of health effects, including cancer, liver and kidney damage, developmental delays, and immune system dysfunction. Because PFAS do not break down easily, they can accumulate in the body over time and remain there for years.")
st.sidebar.subheader("What is currently being done?") 
st.sidebar.info("Efforts are underway to regulate and phase out the use of PFAS in products, and to clean up contaminated sites. However, the widespread use of these chemicals over many decades means that they will continue to pose a challenge for the environment and human health for years to come.")

# App Aesthetics

html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">PFAS Water Contamination Monitoring App</h2>
    </div>
    """
st.markdown(html_temp,unsafe_allow_html=True)


st.write("")
st.write("")


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


Substance_type = data["Chemical"].unique()

st.write("")
st.write("")

# Selection Box for Different Substances
substances = st.multiselect(
    "Select PFAS for Geographic Distribution:",
    options = Substance_type,
    default = ["PFOS"]
)

filtered_data = data[data['Chemical'].isin(substances)]

# Create a dictionary to map each substance to its corresponding color
substance_color_map = {substance: substance_colors[substance] for substance in filtered_data['Chemical'].unique()}

st.write("")
st.write("")

subset = data[data["Chemical"].isin(substances)]

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
    color=alt.Color("Chemical:N", scale=alt.Scale(domain=list(substance_color_map.keys()), range=list(substance_color_map.values()))),
    size=alt.value(160),   
    tooltip=[alt.Tooltip('Towns:N', title='Location'), alt.Tooltip('Chemical:N', title='Substance'),alt.Tooltip('Levels:N', title='Level')])
Map_chart = Map + points



# Filter subsetted data based on selected year and substances
subset_filtered = subset.loc[(subset['Year'] == year) & (subset['Chemical'].isin(substances)), :]
subset_filtered.Year = subset_filtered.Year.astype(str)

# Row A
st.markdown('### Massachusetts PFAS Contaminations')
st.write("")
col1, col2, col3 = st.columns(3)
col1.metric("Most Contaminated Town", subset_filtered[["Year", "Towns","Chemical","Levels"]].sort_values(by="Levels", ascending=False).drop_duplicates(subset="Towns").reset_index(drop=True).iloc[0,1])
col2.metric("Top PFAS", subset_filtered[["Year", "Towns","Chemical","Levels"]].sort_values(by="Levels", ascending=False).drop_duplicates(subset="Towns").reset_index(drop=True).iloc[0,2])
col3.metric("Highest Recorded Level", str(subset_filtered[["Year", "Towns","Chemical","Levels"]].sort_values(by="Levels", ascending=False).drop_duplicates(subset="Towns").reset_index(drop=True).iloc[0,3])+" ng/L")

st.altair_chart(Map_chart, use_container_width=True)

html_temp = """
    <div style="background-color:salmon;padding:10px">
    <h2 style="color:white;text-align:center;">Top PFAS Contaminants by Town</h2>
    </div>
    """
st.markdown(html_temp,unsafe_allow_html=True)

# Show filtered data in a table
st.dataframe(subset_filtered[["Year", "Towns","Chemical","Levels"]].sort_values(by="Levels", ascending=False).drop_duplicates(subset="Towns").reset_index(drop=True), width=1000)
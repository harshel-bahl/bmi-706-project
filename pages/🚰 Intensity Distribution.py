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

# multi-selector to choose which years to display on chart
selectedYears = st.multiselect("Years Shown", poss_years, default=poss_years[0], max_selections=2)

if len(selectedYears) == 0:
    st.error("Please select at least one option.")
    selectedYears = [2019]

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

selectedLevelGroup = st.slider("Inverse Cumulative Groups(A value of 80 will show the top 20% of contaminated regions)", min_value=0, max_value=90, step=10, value=50)

subData = subData[subData["LevelGroup"]==selectedLevelGroup]

# Intensity Map: intensity of PFAs overlayed across the base map of Massachussetts
base = alt.Chart(data_map).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('mercator').properties(
    width=800,
    height=400
)

# add threshold levels in place of quantiles for interpretability

markSchemes = ["circle", "square", "point"]

def createChart(inputData, markScheme, colorScheme):

    levelsScale = alt.Scale(domain=[inputData['Levels'].quantile(0.1), inputData['Levels'].quantile(0.9)], scheme=colorScheme, clamp=True)
    levelsColor = alt.Color(field='Levels', type='quantitative', scale=levelsScale, legend=alt.Legend(title="Contamination Levels"))

    points = alt.Chart(inputData, mark=markScheme).encode(
        longitude='Longitude:Q',
        latitude='Latitude:Q',
        color=levelsColor,
        size=alt.value(100),
        opacity=alt.value(0.5),
        tooltip='Towns'
    )

    return points

if len(selectedYears)==1:

    st.markdown('### '+ str(selectedYears[0]))
    chart1 = base + createChart(subData[subData["Year"]==selectedYears[0]], markSchemes[0], "blues")
    st.altair_chart(chart1, use_container_width=True)


if len(selectedYears)==2:

    st.markdown('### '+str(selectedYears[0]))
    chart1 = base + createChart(subData[subData["Year"]==selectedYears[0]], markSchemes[0], "blues")
    st.altair_chart((chart1), use_container_width=True)

    st.markdown('### '+str(selectedYears[1]))
    chart2 = base + createChart(subData[subData["Year"]==selectedYears[1]], markSchemes[1], "oranges")
    st.altair_chart((chart2), use_container_width=True)
    





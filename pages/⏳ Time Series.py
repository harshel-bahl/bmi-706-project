import altair as alt
import pandas as pd
import streamlit as st

# Time Series Chart - show PFA levels over time for a given site
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

# st.write("PFA Levels over time")

# Pre-processing - get relevant unique values for columns and scale levels
data1 = pd.read_csv("final_mass_data.csv")

siteslist = data1['Towns'].unique()
site_select = st.selectbox(label="Towns", options=siteslist, index=0)

data = data1[data1["Towns"]==site_select]

chemicalslist = data1['Abbreviation'].unique()

chemicals = st.multiselect(label="Chemical", options = chemicalslist, default="PFOS")

data = data[data["Abbreviation"].isin(chemicals)]

selector = alt.selection_single( fields = ['Chemical'])

data["Date"] = data["Date"].str.replace("T.*", "", regex=True)

base = alt.Chart(data).properties().encode(
    x=alt.X('Date:T'),
    y=alt.Y('Levels:Q'),
    color=alt.Color('Abbreviation:N')
).add_selection(selector).transform_filter(selector)

brush = alt.selection_interval(encodings=['x'])

upper = base.mark_line(point=True).encode(
    alt.X('Date:T', scale = alt.Scale(domain=brush))
).transform_filter(brush)

lower = base.mark_bar().add_selection(brush)

lower=lower.properties(height=50)

chart1 = upper & lower

st.altair_chart(chart1, use_container_width=True)

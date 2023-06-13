import streamlit as st
import pycountry
import plotly.express as px
import plotly.colors as colors
import pandas as pd

#page layout
st.set_page_config(page_title="Mean ESG Scores by Years and Countries", page_icon=":guardsman:", layout="wide")

# Add headline and subheader
st.title("Mean ESG Scores by Years and Countries")
st.subheader("Brought to you by Chia-Jung, Ian, Neelesh and Nils, a team of data science students at Frankfurt School")
st.subheader("The basis for this plot are the ESG scores of nearly 7.000 companies (>50.000 observations)")

# ----------- Step 1 ------------
df_raw = pd.read_csv("main_df_no_NAN_99p.csv")
float_columns = df_raw.select_dtypes(include=['float64'])
index_columns = df_raw[["Country of Headquarters", "Year"]]
df = pd.concat([float_columns, index_columns], axis=1)
df = df.groupby(["Country of Headquarters", "Year"]
                ).mean().reset_index().sort_values(by="Year")

# ----------- Step 2 ------------
list_countries = df['Country of Headquarters'].unique().tolist()

d_country_code = {}
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        print('could not add ISO 3 code for ->', country)
        d_country_code.update({country: ' '})

for k, v in d_country_code.items():
    df.loc[(df["Country of Headquarters"] == k), 'iso_alpha'] = v

# ----------- Step 3 ------------
fig = px.choropleth(data_frame=df,
                    locations="iso_alpha",
                    color="ESG Score",
                    hover_name="Country of Headquarters",
                    color_continuous_scale=colors.diverging.RdYlGn,
                    range_color=[0, 100],
                    animation_frame="Year",
                    width=1300, height=750)

# Display the plot in Streamlit
#st.plotly_chart(fig)

# Create a centered container
container = st.container()
with container:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        # Display the plot inside the centered container
        st.plotly_chart(fig, use_container_width=True)
import pandas as pd
import streamlit as st
import plotly.express as px
df = pd.read_csv('zomato.csv')
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]
df['Country Name'] = df['Country Code'].apply(country_name)
df["Cuisines"] = df.loc[:, "Cuisines"].apply(lambda x: str(x).split(",")[0])
# filtros
st.sidebar.title('Filtros')
country_name2 = st.sidebar.multiselect(
    'Selecione os países:',
    options=df.loc[:, 'Country Name'].dropna().unique().tolist(),
    default=df.loc[:, 'Country Name'].dropna().unique().tolist()    
)
linha2 = df['Country Name'].isin(country_name2)
df = df.loc[linha2, :]

# Layout no streamlit

st.title('🌍Visão países')

st.subheader('Quantidade de restaurantes registrados por país')
df_aux = df.loc[:, ['Restaurant ID', 'Country Name']].groupby('Country Name').count().reset_index()
fig = px.bar(df_aux, x='Country Name', y='Restaurant ID')
st.plotly_chart(fig, use_container_width=True)

st.subheader('Quantidade de cidades registradas por país')
df_aux2 = df.loc[:, ['Country Name', 'City']].groupby('Country Name').agg({'City' : 'nunique'}).reset_index()
fig = px.bar(df_aux2, x='Country Name', y='City')
st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Média de avaliações feitas por país')
        
        df_aux3 = df.loc[:, ['Votes', 'Country Name']].groupby('Country Name').mean().reset_index()
        fig = px.bar(df_aux3, x='Country Name', y='Votes')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader('Média de preço de um prato para duas pessoas por país')
        df_aux4 = df.loc[:, ['Average Cost for two', 'Country Name']].groupby('Country Name').mean().reset_index()
        fig = px.bar(df_aux4, x='Country Name', y='Average Cost for two')
        st.plotly_chart(fig, use_container_width=True)
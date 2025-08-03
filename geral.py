import pandas as pd
import streamlit as st
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


# layout no streamlit
st.title('Fome Zero')
st.subheader('Maior rede de restaurantes da américa latina')

st.markdown('## Temos as seguintes marcas na nossa plataforma')
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        rest = df['Restaurant ID'].nunique()
        col1.metric('Restaurantes cadastrados', rest)

    with col2:

        paises = df['Country Name'].nunique()
        col2.metric('Países cadastrados', paises)

    with col3:
        city = df['City'].nunique()
        col3.metric('Cidades cadastradas', city)

    with col4:
        avaliacoes = sum(df['Rating color'].value_counts())
        col4.metric('Avaliações já feitas', avaliacoes)

    with col5:
        cuisines = df['Cuisines'].nunique()
        col5.metric('Tipos de culinária', cuisines)
    
df_aux = (
    df[['Restaurant Name', 'Latitude', 'Longitude']]
    .groupby('Restaurant Name')
    .agg({'Latitude': 'first', 'Longitude': 'first'})
    .reset_index())



st.map(df_aux, latitude='Latitude', longitude='Longitude', size=800)

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


# layout no streamlit
st.title('🏙️Visão Cidade')
st.markdown('## Top 10 Cidades com mais Restaurantes')

df2 = (
    df.loc[:, ['Restaurant ID', 'City']]
      .groupby('City', sort=True)['Restaurant ID']  # garante ordenação por cidade
      .nunique()
      .reset_index(name='count')
      .sort_values(by='count', ascending=True))
fig = px.bar(df2.head(10), x='City', y='count')
fig.update_coloraxes(cmin=df2['count'].min(), cmax=df2['count'].max())
st.plotly_chart(fig)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Cidades com Restaurantes com média de avaliação acima de 3')
        df_aux = (df.loc[:, ['Aggregate rating', 'City']].groupby('City', sort=True).mean().reset_index().sort_values(by='Aggregate rating', ascending=True))
        linha = df_aux['Aggregate rating'] > 3.0
        df_aux = df_aux.loc[linha, ['City', 'Aggregate rating']]
        fig = px.bar(df_aux.head(7), x='City', y='Aggregate rating')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader('Cidades com Restaurantes com média de avaliação abaixo de 3')
        df_aux = (df.loc[:, ['Aggregate rating', 'City']].groupby('City', sort=False).mean().reset_index().sort_values(by='Aggregate rating', ascending=False))
        linha = df_aux['Aggregate rating'] < 3.0
        df_aux = df_aux.loc[linha, ['City', 'Aggregate rating']]
        fig2 = px.bar(df_aux.head(7), x='City', y='Aggregate rating')
        st.plotly_chart(fig2, use_container_width=True)

st.subheader('Top 10 Cidades com mais tipos de culinárias diferentes')
df_aux1 = (df.loc[:, ['Cuisines', 'City']].groupby('City', sort=True).nunique().reset_index().sort_values(by='City', ascending=True))
fig = px.bar(df_aux1.head(10), x='City', y='Cuisines')
st.plotly_chart(fig)
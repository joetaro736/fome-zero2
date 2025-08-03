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

total_restaurantes = df['Restaurant ID'].nunique()


# Slider: quantos restaurantes visualizar
num_restaurantes = st.sidebar.slider(
    "Selecione a quantidade de restaurantes a exibir:",
    min_value=0,
    max_value=total_restaurantes,
    value=total_restaurantes
)


# Seleciona os primeiros N IDs únicos
ids_selecionados = df['Restaurant ID'].drop_duplicates().head(num_restaurantes)

# Filtra o DataFrame
df = df[df['Restaurant ID'].isin(ids_selecionados)]

cuisines = st.sidebar.multiselect(
    'Selecione os tipos de comida:',
    options=df.loc[:, 'Cuisines'].dropna().unique().tolist(),
    default=df.loc[:, 'Cuisines'].dropna().unique().tolist()    
)

df_aux = (df.loc[:, ['Aggregate rating', 'Cuisines']].groupby('Cuisines', sort=True).max().reset_index().sort_values(by='Aggregate rating', ascending=True))
df_aux = df_aux.loc[:, ['Cuisines', 'Aggregate rating']]

linha2 = df['Cuisines'].isin(cuisines)
df = df.loc[linha2, :]

# layout no streamlit

st.title('🍽️Cuisines')
df_aux = (
    df.loc[:, ['Cuisines', 'Aggregate rating', 'Restaurant Name']]
      .sort_values(by='Aggregate rating', ascending=False)  # Ordena do melhor para o pior
      .drop_duplicates(subset='Cuisines')                   # Pega o melhor restaurante por culinária
      .reset_index(drop=True)
      .head(5)                                              # Pega os 5 com maior nota entre os melhores de cada tipo
)

st.subheader('Melhores restaurantes por tipo de culinária')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i, row in df_aux.iterrows():
        with cols[i]:
            st.metric(
                label=f"{row['Cuisines']}: {row['Restaurant Name']}",
                value=f"{row['Aggregate rating']}/5.0"
            )

st.subheader('Top 10 melhores Restaurantes')

df_aux2 = (
    df.loc[:, :]
      .sort_values(by='Aggregate rating', ascending=False)  # Ordena do melhor para o pior
      .reset_index(drop=True)
)

st.dataframe(df_aux2.head(10))

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Top 10 melhores tipos de culinária')
        # Agrupa o DataFrame original e calcula a média das avaliações por tipo de culinária
        df_aux2 = (
    df.loc[:, ['Cuisines', 'Aggregate rating']]
      .groupby('Cuisines')
      .mean(numeric_only=True)
      .reset_index()
      .sort_values(by='Aggregate rating', ascending=False)
      .head(10)
)
        fig = px.bar(df_aux2, x='Cuisines', y='Aggregate rating')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader('Top 10 piores tipos de culinária')
        # Filtra colunas e remove valores nulos ou "nan" como string
        df_clean = df.loc[:, ['Cuisines', 'Aggregate rating']].dropna()
        df_clean = df_clean[~df_clean['Cuisines'].str.strip().str.lower().eq('nan')]

        # Agrupa por tipo de culinária e calcula a média das avaliações
        df_aux2 = (
    df_clean
      .groupby('Cuisines')
      .mean(numeric_only=True)
      .reset_index()
      .sort_values(by='Aggregate rating', ascending=True)
      .head(10)
)
        fig = px.bar(df_aux2, x='Cuisines', y='Aggregate rating')
        st.plotly_chart(fig, use_container_width=True)
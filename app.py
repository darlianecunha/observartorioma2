import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Carregar estilos CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Adicionando um ícone de navio no topo
st.markdown("""
<div class='navio'>
    <img src='https://cdn-icons-png.flaticon.com/128/2866/2866321.png' width='80'>
</div>
""", unsafe_allow_html=True)

# Cabeçalho do Dashboard
st.markdown("<h1>Dashboard de Movimentação Portuária - Maranhão 2010 a 2023</h1>", unsafe_allow_html=True)

# Carregar os dados
@st.cache_data
def load_data():
    file_path = "movMA2023.xlsx"
    if not os.path.exists(file_path):
        st.error(f"Erro: Arquivo {file_path} não encontrado!")
        return pd.DataFrame()
    
    df = pd.read_excel(file_path)
    df.rename(columns={
        'Ano': 'ano',
        'Tipo de instalação': 'tipo_instalacao',
        'Nome da Instalação': 'nome_instalacao',
        'Perfil da Carga': 'perfil_carga',
        'Nomenclatura Simplificada': 'nomenclatura_simplificada',
        'Sentido': 'sentido',
        'Tipo Navegação': 'tipo_navegacao',
        'Total de Movimentação Portuária\nem milhões x t': 'movimentacao_milhoes_t'
    }, inplace=True)
    df["ano"] = df["ano"].astype(str)
    return df

df = load_data()

# Filtros
st.sidebar.header("Filtros")
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", sorted(df["ano"].dropna().unique()), index=0)
tipo_instalacao_selecionado = st.sidebar.selectbox("Selecione o Tipo de Instalação", ["Todos"] + list(df["tipo_instalacao"].dropna().unique()), index=0)
nome_instalacao_selecionado = st.sidebar.selectbox("Selecione a Instalação", ["Todos"] + list(df["nome_instalacao"].dropna().unique()), index=0)
perfil_carga_selecionado = st.sidebar.selectbox("Selecione o Perfil da Carga", ["Todos"] + list(df["perfil_carga"].dropna().unique()), index=0)
sentido_selecionado = st.sidebar.selectbox("Selecione o Sentido", ["Todos"] + list(df["sentido"].dropna().unique()), index=0)
tipo_navegacao_selecionado = st.sidebar.selectbox("Selecione o Tipo de Navegação", ["Todos"] + list(df["tipo_navegacao"].dropna().unique()), index=0)
nomenclatura_simplificada_selecionado = st.sidebar.selectbox("Selecione a Nomenclatura Simplificada", ["Todos"] + list(df["nomenclatura_simplificada"].dropna().unique()), index=0)

# Aplicar filtros
df_filtered = df[df["ano"] == ano_selecionado]
if tipo_instalacao_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["tipo_instalacao"] == tipo_instalacao_selecionado]
if nome_instalacao_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["nome_instalacao"] == nome_instalacao_selecionado]
if perfil_carga_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["perfil_carga"] == perfil_carga_selecionado]
if sentido_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["sentido"] == sentido_selecionado]
if tipo_navegacao_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["tipo_navegacao"] == tipo_navegacao_selecionado]
if nomenclatura_simplificada_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["nomenclatura_simplificada"] == nomenclatura_simplificada_selecionado]

# Criar gráfico interativo com Plotly
if not df_filtered.empty:
    fig = px.bar(
        df_filtered,
        x="nome_instalacao",
        y="movimentacao_milhoes_t",
        color="perfil_carga",
        title="Movimentação por Instalação",
        labels={"movimentacao_milhoes_t": "Milhões de Toneladas"}
    )
    st.plotly_chart(fig, use_container_width=True)

# Exibir tabela de dados agregados
st.write("### Movimentação Total por Porto")
st.dataframe(df_filtered, width=800)

# Crédito
st.write("Fonte: Estatístico Aquaviário ANTAQ")
st.markdown("<p><strong>Ferramenta desenvolvida para o Observatório Portuário com Financiamento do Itaqui </strong></p>", unsafe_allow_html=True)



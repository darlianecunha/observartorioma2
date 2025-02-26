import streamlit as st
import pandas as pd

# Definir estilo global com fundo branco e títulos azul escuro
st.markdown(
    """
    <style>
        body {
            background-color: white;
            color: black;
        }
        h1, h2 {
            color: #003366;
            text-align: center;
        }
        .stDataFrame, .stTable {
            background-color: white;
            color: black;
        }
        .navio {
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Adicionando um ícone de navio no topo
topo_html = """
<div class='navio'>
    <img src='https://cdn-icons-png.flaticon.com/128/2866/2866321.png' width='80'>
</div>
"""
st.markdown(topo_html, unsafe_allow_html=True)

# Cabeçalho do Dashboard
st.markdown("<h1>Dashboard de Movimentação Portuária - Maranhão 2010 a 2023</h1>", unsafe_allow_html=True)

# Carregar os dados
@st.cache_data
def load_data():
    file_path = "movMA2023.xlsx" 
    df = pd.read_excel(file_path)
    df = df.rename(columns={
        'Ano': 'ano',
        'Tipo de instalação': 'tipo_instalacao',
        'Nome da Instalação': 'nome_instalacao',
        'Perfil da Carga': 'perfil_carga',
        'Nomenclatura Simplificada': 'nomenclatura_simplificada',
        'Sentido': 'sentido',
        'Tipo Navegação': 'tipo_navegacao',
        'Total de Movimentação Portuária\nem milhões x t': 'movimentacao_milhoes_t'
    })
    df["ano"] = df["ano"].astype(str)  # Garantir formato correto de ano
    return df

df = load_data()

# Filtros
st.sidebar.header("Filtros")
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", sorted(df["ano"].unique()), index=0)
tipo_instalacao_selecionado = st.sidebar.selectbox("Selecione o Tipo de Instalação", ["Todos"] + list(df["tipo_instalacao"].unique()), index=0)
nome_instalacao_selecionado = st.sidebar.selectbox("Selecione a Instalação", ["Todos"] + list(df["nome_instalacao"].unique()), index=0)
perfil_carga_selecionado = st.sidebar.selectbox("Selecione o Perfil da Carga", ["Todos"] + list(df["perfil_carga"].unique()), index=0)
sentido_selecionado = st.sidebar.selectbox("Selecione o Sentido", ["Todos"] + list(df["sentido"].unique()), index=0)
tipo_navegacao_selecionado = st.sidebar.selectbox("Selecione o Tipo de Navegação", ["Todos"] + list(df["tipo_navegacao"].unique()), index=0)
nomenclatura_simplificada_selecionado = st.sidebar.selectbox("Selecione a Nomenclatura Simplificada", ["Todos"] + list(df["nomenclatura_simplificada"].unique()), index=0)

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

# Agregar dados por instalação
df_summary = df_filtered.groupby(["nome_instalacao"], as_index=False)["movimentacao_milhoes_t"].sum()

# Soma total da movimentação portuária
total_movimentacao = df_summary["movimentacao_milhoes_t"].sum()

# Formatar os números para exibição no padrão brasileiro
df_summary["movimentacao_milhoes_t"] = df_summary["movimentacao_milhoes_t"].apply(lambda x: f"{x:,.3f}".replace(",", "."))
total_movimentacao = f"{total_movimentacao:,.3f}".replace(",", ".")

# Exibir tabela de dados agregados
st.write("### Movimentação Total por Porto")
st.dataframe(df_summary, width=800)

# Exibir total de movimentação
st.markdown(f"""
    <h2>Movimentação Total: {total_movimentacao} milhões de toneladas</h2>
    """, unsafe_allow_html=True)

# Crédito 
st.write("Fonte: Estatístico Aquaviário ANTAQ")
st.markdown("<p><strong>Ferramenta desenvolvida para o Observatório Portuário com Financiamento do Itaqui </strong></p>", unsafe_allow_html=True)


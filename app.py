from shiny import App, ui, render
import pandas as pd
import plotly.express as px
import os

# Interface do Usuário (UI)
app_ui = ui.page_fluid(
    ui.h1("Dashboard de Movimentação Portuária - Maranhão 2010 a 2023"),
    ui.input_select("ano", "Selecione o Ano", choices=[]),
    ui.input_select("tipo_instalacao", "Selecione o Tipo de Instalação", choices=["Todos"]),
    ui.input_select("nome_instalacao", "Selecione a Instalação", choices=["Todos"]),
    ui.input_select("perfil_carga", "Selecione o Perfil da Carga", choices=["Todos"]),
    ui.input_select("sentido", "Selecione o Sentido", choices=["Todos"]),
    ui.input_select("tipo_navegacao", "Selecione o Tipo de Navegação", choices=["Todos"]),
    ui.input_select("nomenclatura_simplificada", "Selecione a Nomenclatura Simplificada", choices=["Todos"]),
    ui.output_plot("grafico"),
    ui.output_data_frame("tabela"),
    ui.output_text_verbatim("total_movimentacao")
)

# Lógica do Servidor
def server(input, output, session):

    # Carregar dados
    def load_data():
        file_path = "movMA2023.xlsx"
        if not os.path.exists(file_path):
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

    # Atualizar opções dos filtros dinamicamente
    @render.ui
    def ano():
        return ui.input_select("ano", "Selecione o Ano", choices=sorted(df["ano"].dropna().unique()), selected=df["ano"].iloc[0])

    @render.ui
    def tipo_instalacao():
        return ui.input_select("tipo_instalacao", "Selecione o Tipo de Instalação", choices=["Todos"] + list(df["tipo_instalacao"].dropna().unique()))

    # Aplicar filtros
    @render.data_frame
    def tabela():
        df_filtered = df[df["ano"] == input.ano()]
        if input.tipo_instalacao() != "Todos":
            df_filtered = df_filtered[df_filtered["tipo_instalacao"] == input.tipo_instalacao()]
        return df_filtered[["nome_instalacao", "movimentacao_milhoes_t"]]

    # Criar gráfico
    @render.plot
    def grafico():
        df_filtered = df[df["ano"] == input.ano()]
        if input.tipo_instalacao() != "Todos":
            df_filtered = df_filtered[df_filtered["tipo_instalacao"] == input.tipo_instalacao()]

        fig = px.bar(
            df_filtered,
            x="nome_instalacao",
            y="movimentacao_milhoes_t",
            color="perfil_carga",
            title="Movimentação por Instalação",
            labels={"movimentacao_milhoes_t": "Milhões de Toneladas"}
        )
        return fig

    @render.text
    def total_movimentacao():
        return f"Movimentação Total: {df['movimentacao_milhoes_t'].sum():,.3f} milhões de toneladas"

# Criando o App
app = App(app_ui, server)

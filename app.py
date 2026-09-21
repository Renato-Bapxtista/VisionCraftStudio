"""
Modulo: app.py
Descricao: Ponto de entrada da aplicacao Streamlit.
"""

import streamlit as st

from estado import inicializar_estado
from componentes.cabecalho import renderizar_cabecalho
from componentes.upload import renderizar_upload
from componentes.visualizacao import renderizar_visualizacao
from componentes.historico import renderizar_historico
from componentes.ferramentas import renderizar_ferramentas
from componentes.histograma import renderizar_histograma

def carregar_css(caminho_css: str):
    """Lê um ficheiro CSS local e injeta-o na aplicação Streamlit."""
    with open(caminho_css, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 1. Configuracao basica da pagina no navegador
st.set_page_config(page_title="Processador de Imagem", layout="wide")

# 2. Carregar o estilo visual externo
carregar_css("estilos.css")

# 3. Inicializa as variaveis na memoria do Streamlit
inicializar_estado()

# 4. Renderizar o componente de Cabeçalho
renderizar_cabecalho()
    
# 5. Estrutura de Layout em 3 Colunas
col_esquerda, col_centro, col_direita = st.columns([1, 2.8, 1.2])

with col_esquerda:
    # Renderiza o botão de upload e miniatura da imagem original
    renderizar_upload()
    renderizar_historico()

with col_centro:
    # Renderiza a pré-visualização central[cite: 1]
    renderizar_visualizacao()

with col_direita:
    # Renderiza o painel interativo de filtros e ajustes
    renderizar_ferramentas()
    renderizar_histograma()
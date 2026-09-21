"""
Modulo: app.py
Descricao: Ponto de entrada da aplicacao Streamlit.
"""

import streamlit as st
from estado import inicializar_estado
from componentes.cabecalho import renderizar_cabecalho

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

# 5. Estrutura temporária para testar o layout
st.info("Passo 2 concluído: CSS e Cabeçalho renderizados com sucesso!")
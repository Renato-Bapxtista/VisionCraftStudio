"""
Modulo: app.py
Descricao: Ponto de entrada da aplicacao Streamlit.
"""

import os
import sys

# Adiciona o diretório raiz ao sys.path para permitir a importação dos módulos da raiz (estado, componentes, processamento)
DIRETORIO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if DIRETORIO_RAIZ not in sys.path:
    sys.path.insert(0, DIRETORIO_RAIZ)

import streamlit as st

from src.estado import inicializar_estado
from componentes.cabecalho import renderizar_cabecalho
from componentes.upload import renderizar_upload
from componentes.visualizacao import renderizar_visualizacao
from componentes.historico import renderizar_historico
from componentes.ferramentas import renderizar_ferramentas
from componentes.histograma import renderizar_histograma

def carregar_css(caminho_css: str):
    """Lê um ficheiro CSS local e injeta-o na aplicação Streamlit."""
    if os.path.exists(caminho_css):
        with open(caminho_css, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 1. Configuracao basica da pagina no navegador
st.set_page_config(page_title="Processador de Imagem", layout="wide")

# 2. Carregar o estilo visual externo da pasta static
caminho_estilos = os.path.join(DIRETORIO_RAIZ, "static", "estilos.css")
carregar_css(caminho_estilos)

# 3. Inicializa as variaveis na memoria do Streamlit
inicializar_estado()

# 4. Renderizar o componente de Cabeçalho
renderizar_cabecalho()
    
# 5. Estrutura de Layout em 3 Colunas
col_esquerda, col_centro, col_direita = st.columns([1, 2.8, 1.2])

with col_esquerda:
    # 1. Topo fixo da coluna esquerda: Upload de Imagem e Ações do Histórico
    renderizar_upload()
    renderizar_historico()

with col_centro:
    # 2. Área central: Pré-visualização fixa da imagem
    renderizar_visualizacao()

with col_direita:
    # 3. Topo fixo da coluna direita: Rádio "Aplicar Em"
    st.markdown("<div class='figma-label'>FERRAMENTAS</div>", unsafe_allow_html=True)
    if st.session_state.img_atual is not None:
        st.markdown("<div class='figma-label'>APLICAR EM</div>", unsafe_allow_html=True)
        alvo_op = st.radio(
            "Selecione o alvo:",
            ("Última Processada", "Original"),
            index=0,
            key="alvo_operacao_fixo",
            label_visibility="collapsed"
        )
        st.session_state.alvo_op_global = alvo_op
    else:
        st.info("Aguardando carregamento de imagem...")

    # Área de ferramentas expansíveis com scroll independente
    if st.session_state.img_atual is not None:
        with st.container(height=340, border=False):
            renderizar_ferramentas()
        
        # Histograma fixo na parte inferior da coluna direita
        renderizar_histograma()
"""
Modulo: estado.py
Descricao: Responsavel por inicializar e gerenciar as variaveis de memoria 
(session_state) da aplicacao Streamlit.
"""

import streamlit as st


def inicializar_estado():
    """Inicializa as variaveis globais da sessao caso ainda nao existam."""
    # Guarda a imagem original sem alteracoes
    if 'img_original' not in st.session_state:
        st.session_state.img_original = None

    # Guarda a imagem com os filtros aplicados atualmente
    if 'img_atual' not in st.session_state:
        st.session_state.img_atual = None

    # Guarda a lista com o historico de etapas aplicadas (pipeline)
    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = []

    # Guarda o indice da etapa ativa no historico
    if 'active_index' not in st.session_state:
        st.session_state.active_index = 0

    # Guarda o identificador do ultimo ficheiro enviado para evitar recarregamentos desnecessarios
    if 'last_uploaded' not in st.session_state:
        st.session_state.last_uploaded = None

    # Guarda metadados da imagem (largura, altura, formato)
    if 'img_info' not in st.session_state:
        st.session_state.img_info = None
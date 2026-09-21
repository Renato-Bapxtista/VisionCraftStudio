"""
Modulo: componentes/cabecalho.py
Descricao: Componente responsavel por renderizar a barra superior da interface.
"""

import streamlit as st


def renderizar_cabecalho(titulo: str = "Processador de Imagem", subtitulo: str = "VisionCraft Studio"):
    """
    Renderiza o cabecalho customizado utilizando as classes CSS definidas em estilos.css.
    
    Parametros:
        titulo (str): Titulo principal exibido a esquerda.
        subtitulo (str): Nome do modulo ou versao exibido a direita.
    """
    html_code = f"""
    <div class="figma-header">
        <span style="font-size: 0.95rem; font-weight: 700; color: #111827;">{titulo}</span>
        <span style="font-size: 0.75rem; color: #6B7280;">{subtitulo}</span>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
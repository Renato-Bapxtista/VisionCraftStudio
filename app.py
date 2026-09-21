"""
Modulo: app.py
Descricao: Ponto de entrada da aplicacao Streamlit.
"""

import streamlit as st
from estado import inicializar_estado

# 1. Configuracao basica da pagina no navegador
st.set_page_config(page_title="Processador de Imagem", layout="wide")

# 2. Inicializa as variaveis na memoria do Streamlit
inicializar_estado()

# 3. Mensagem de teste para confirmar que o passo 1 funcionou
st.title(" Processador de Imagem")
st.success("O estado da aplicacao foi inicializado com sucesso!")

# Exibe o estado atual para confirmacao visual
st.write("Estado atual da sessao:", st.session_state)
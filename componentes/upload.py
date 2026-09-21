"""
Módulo: componentes/upload.py
Descrição: Componente responsável pelo carregamento de imagens e conversão para NumPy.
"""

import hashlib
import io
import numpy as np
import streamlit as st
from PIL import Image, UnidentifiedImageError
from estado import registrar_nova_etapa


def renderizar_upload():
    """
    Exibe o seletor de ficheiros na interface e processa a imagem carregada.
    Guarda a matriz da imagem e os seus metadados no st.session_state[cite: 1].
    """
    st.markdown("<div class='figma-label'>IMAGEM</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Carregar Imagem",
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        dados_upload = uploaded_file.getvalue()
        identificador_upload = hashlib.sha256(dados_upload).hexdigest()

        if st.session_state.last_uploaded != identificador_upload:
            try:
                with Image.open(io.BytesIO(dados_upload)) as img:
                    img.load()
                    formato = img.format or "Desconhecido"
                    possui_transparencia = img.mode in ("RGBA", "LA") or "transparency" in img.info

                    if possui_transparencia:
                        img_processavel = img.convert("RGBA")
                    elif img.mode == "L":
                        img_processavel = img.convert("L")
                    else:
                        img_processavel = img.convert("RGB")

                    matriz_img = np.array(img_processavel)

                altura, largura = matriz_img.shape[:2]

                st.session_state.img_original = matriz_img
                st.session_state.pipeline = []
                st.session_state.active_index = 0

                # Chama a função definida em estado.py
                registrar_nova_etapa("Carregamento Inicial", matriz_img)

                st.session_state.img_info = {
                    "nome": uploaded_file.name,
                    "formato": formato,
                    "modo": img_processavel.mode,
                    "largura": largura,
                    "altura": altura,
                    "transparencia": possui_transparencia,
                }
                st.session_state.last_uploaded = identificador_upload
                st.rerun()

            except (UnidentifiedImageError, OSError, ValueError):
                st.error("Não foi possível abrir esta imagem. Envia um ficheiro PNG ou JPG válido.")
    else:
        if st.session_state.img_original is not None:
            st.session_state.img_original = None
            st.session_state.img_atual = None
            st.session_state.pipeline = []
            st.session_state.active_index = 0
            st.session_state.last_uploaded = None
            st.session_state.img_info = None
            st.rerun()

    if st.session_state.img_original is not None:
        info = st.session_state.img_info
        if info:
            transparencia = " • Transparência preservada" if info["transparencia"] else ""
            st.caption(
                f"**{info['nome']}**\n\n"
                f"{info['largura']} × {info['altura']} px • "
                f"{info['formato']} • {info['modo']}{transparencia}"
            )
        st.image(st.session_state.img_original, use_container_width=True)
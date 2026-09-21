"""
Módulo: componentes/visualizacao.py
Descrição: Exibição da imagem processada e comparação lado a lado sem avisos de depreciação.
"""

import streamlit as st


def _imagem_valida(matriz_img) -> bool:
    """Verifica se a matriz da imagem possui dimensões válidas."""
    if matriz_img is None:
        return False
    if not hasattr(matriz_img, "shape") or len(matriz_img.shape) < 2:
        return False
    return matriz_img.shape[0] > 0 and matriz_img.shape[1] > 0


def renderizar_visualizacao():
    """Renderiza a área central de pré-visualização da imagem."""
    st.markdown("<div class='figma-label'>PRÉ-VISUALIZAÇÃO</div>", unsafe_allow_html=True)

    if st.session_state.img_atual is not None:
        img_atual = st.session_state.img_atual
        img_orig = st.session_state.img_original

        if not _imagem_valida(img_atual):
            st.warning(
                "⚠️ A imagem resultante possui dimensões inválidas (altura ou largura igual a 0). "
                "Utilize o painel de histórico à esquerda para desfazer a última operação."
            )
            return

        st.caption("Use 'Comparar' para ver a imagem original e o resultado lado a lado.")
        
        modo_visualizacao = st.radio(
            "Modo de visualização",
            ("Resultado", "Comparar"),
            horizontal=True,
            label_visibility="collapsed"
        )

        try:
            if modo_visualizacao == "Comparar":
                if not _imagem_valida(img_orig):
                    st.error("A imagem original possui dimensões inválidas e não pode ser exibida.")
                    return

                col_orig, col_res = st.columns(2)
                with col_orig:
                    st.caption("ORIGINAL")
                    st.image(img_orig, use_container_width=True)
                with col_res:
                    st.caption("RESULTADO")
                    st.image(img_atual, use_container_width=True)
            else:
                st.image(img_atual, use_container_width=True)

        except Exception:
            st.error(
                "Não foi possível exibir o resultado desta transformação. "
                "Por favor, desfaça a etapa no histórico."
            )
    else:
        st.info("Carregue uma imagem no painel à esquerda para iniciar.")
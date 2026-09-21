"""
Módulo: componentes/visualizacao.py
Descrição: Componente responsável por exibir a imagem atual ou a comparação 
lado a lado entre a original e a processada.
"""

import streamlit as st


def renderizar_visualizacao():
    """
    Renderiza o painel central de pré-visualização da imagem.
    Permite alternar entre o modo 'Resultado' e 'Comparar'[cite: 1].
    """
    st.markdown("<div class='figma-label'>PRÉ-VISUALIZAÇÃO</div>", unsafe_allow_html=True)

    # Verifica se existe uma imagem carregada na memória
    if st.session_state.img_atual is not None:
        st.caption("Use 'Comparar' para ver a imagem original e o resultado lado a lado.")
        
        # Seleção do modo de exibição[cite: 1]
        modo_visualizacao = st.radio(
            "Modo de visualização",
            ("Resultado", "Comparar"),
            horizontal=True,
            label_visibility="collapsed"
        )

        if modo_visualizacao == "Comparar":
            # Cria duas colunas internas para colocar as imagens lado a lado[cite: 1]
            col_orig, col_res = st.columns(2)
            with col_orig:
                st.caption("ORIGINAL")
                st.image(st.session_state.img_original, use_container_width=True)
            with col_res:
                st.caption("RESULTADO")
                st.image(st.session_state.img_atual, use_container_width=True)
        else:
            # Exibe apenas a imagem processada atual[cite: 1]
            st.image(st.session_state.img_atual, use_container_width=True)
    else:
        st.info("Carregue uma imagem no painel à esquerda para iniciar.")
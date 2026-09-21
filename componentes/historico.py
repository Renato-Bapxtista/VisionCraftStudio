"""
Módulo: componentes/historico.py
Descrição: Componente responsável pela navegação no histórico de edições (pipeline)
"""

import streamlit as st
from estado import ir_para_etapa, remover_etapa_atual


def renderizar_historico():
    """
    Renderiza os botões de navegação (Desfazer, Refazer, Remover) 
    e a lista de etapas do histórico na interface
    """
    st.markdown("<div class='figma-label' style='margin-top:10px;'>PIPELINE (HISTÓRICO)</div>", unsafe_allow_html=True)

    if len(st.session_state.pipeline) > 0:
        pode_desfazer = st.session_state.active_index > 0
        pode_refazer = st.session_state.active_index < len(st.session_state.pipeline) - 1

        st.caption("AÇÕES DO HISTÓRICO")
        
        # Botões de Desfazer e Refazer[cite: 1]
        if st.button("Desfazer", disabled=not pode_desfazer, use_container_width=True):
            ir_para_etapa(st.session_state.active_index - 1)
            st.rerun()

        if st.button("Refazer", disabled=not pode_refazer, use_container_width=True):
            ir_para_etapa(st.session_state.active_index + 1)
            st.rerun()

        if st.button(
            "Remover Etapa",
            disabled=not pode_desfazer,
            use_container_width=True,
            help="Remove a etapa ativa e todas as etapas posteriores."
        ):
            remover_etapa_atual()
            st.rerun()

        st.divider()

        # Lista de seleção de etapas gravadas[cite: 1]
        st.caption("ETAPAS DO PROCESSAMENTO")
        opcoes_etapas = list(range(len(st.session_state.pipeline)))
        
        indice_selecionado = st.radio(
            "Selecione uma etapa do histórico",
            opcoes_etapas,
            format_func=lambda i: (
                f"{i + 1}. {st.session_state.pipeline[i]['nome']}"
                f"{' (atual)' if i == st.session_state.active_index else ''}"
            ),
            index=st.session_state.active_index,
            key=f"pipeline_selector_{st.session_state.active_index}_{len(st.session_state.pipeline)}",
            label_visibility="collapsed",
        )

        # Se o utilizador selecionar uma etapa diferente na lista, atualiza a visualização
        if indice_selecionado != st.session_state.active_index:
            ir_para_etapa(indice_selecionado)
            st.rerun()
    else:
        st.caption("Carregue uma imagem para iniciar o histórico.")
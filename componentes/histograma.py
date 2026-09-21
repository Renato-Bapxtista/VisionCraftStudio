"""
Módulo: componentes/histograma.py
Descrição: Componente responsável por gerar e exibir o histograma dos canais de cor
da imagem ativa e disponibilizar o botão de download do resultado.
"""

import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image


def renderizar_histograma():
    """
    Desenha o gráfico de histograma da imagem atual e o botão de salvamento/download.
    """
    if st.session_state.img_atual is None:
        return

    # --- BOTÃO DE DOWNLOAD DA IMAGEM ---
    # Converte a matriz NumPy de volta para uma imagem PIL para salvar
    res_img = Image.fromarray(st.session_state.img_atual)
    res_img.save("temp_download.png")
    
    with open("temp_download.png", "rb") as file:
        st.download_button(
            label="Salvar Imagem Resultado",
            data=file,
            file_name="imagem_processada.png",
            mime="image/png",
            use_container_width=True
        )

    st.divider()

    # --- ANÁLISE DE HISTOGRAMA ---
    st.markdown("<div class='figma-label'>HISTOGRAMA DA IMAGEM</div>", unsafe_allow_html=True)

    img_data = st.session_state.img_atual
    is_gray = len(img_data.shape) == 2 or (len(img_data.shape) == 3 and img_data.shape[2] == 1)

    def gerar_figura(canal_idx=None, cor_grafico='gray'):
        """Função auxiliar para construir a figura Matplotlib do histograma."""
        fig, ax = plt.subplots(figsize=(3.2, 1.3), facecolor='#FFFFFF')
        ax.set_facecolor('#F9FAFB')
        ax.tick_params(colors='#6B7280', labelsize=6)

        if is_gray:
            ax.hist(img_data.ravel(), bins=256, color='gray', alpha=0.7, range=[0, 256])
        elif canal_idx is None:
            # Sobreposição dos 3 canais RGB
            colors = ('#EF4444', '#10B981', '#3B82F6')
            for i, c in enumerate(colors):
                ax.hist(img_data[:, :, i].ravel(), bins=256, color=c, alpha=0.4, range=[0, 256])
        else:
            # Canal individual
            ax.hist(img_data[:, :, canal_idx].ravel(), bins=256, color=cor_grafico, alpha=0.7, range=[0, 256])

        ax.set_xlim([0, 256])
        plt.tight_layout()
        return fig

    # Renderização condicional (Escala de Cinza vs RGB)
    if is_gray:
        fig = gerar_figura()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        aba_rgb, aba_r, aba_g, aba_b = st.tabs(["RGB", "R", "G", "B"])

        with aba_rgb:
            fig = gerar_figura(None)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with aba_r:
            fig = gerar_figura(0, '#EF4444')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with aba_g:
            fig = gerar_figura(1, '#10B981')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with aba_b:
            fig = gerar_figura(2, '#3B82F6')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
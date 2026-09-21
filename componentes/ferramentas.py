"""
Módulo: componentes/ferramentas.py
Descrição: Componente responsável por renderizar os controlos de edição de imagem
(Sliders, Botões e Seletores) na coluna direita da aplicação.
"""

import streamlit as st
from estado import registrar_nova_etapa
from processamento import pontuais, espaciais, geometricas


def renderizar_ferramentas():
    """
    Renderiza os grupos de ferramentas de processamento de imagem em painéis expansíveis.
    """
    st.markdown("<div class='figma-label'>FERRAMENTAS</div>", unsafe_allow_html=True)

    if st.session_state.img_atual is None:
        st.info("Aguardando carregamento de imagem...")
        return

    # Escolha de onde aplicar o efeito (na imagem atual do histórico ou na original)
    st.markdown("<div class='figma-label'>APLICAR EM</div>", unsafe_allow_html=True)
    alvo_op = st.radio(
        "Selecione o alvo:",
        ("Última Processada", "Original"),
        index=0,
        label_visibility="collapsed"
    )

    def obter_base():
        """Retorna uma cópia da imagem base selecionada pelo usuário."""
        if alvo_op == "Original":
            return st.session_state.img_original.copy()
        return st.session_state.img_atual.copy()

    st.write("")

    # --- GRUPOS DE FERRAMENTAS EXPANSÍVEIS ---
    grupo_tom = st.expander("Ajustes de Tom", expanded=True)
    grupo_efeitos = st.expander("Efeitos Visuais")
    grupo_filtros = st.expander("Filtros Espaciais")
    grupo_bordas = st.expander("Detecção de Bordas")
    grupo_geometria = st.expander("Transformações Geométricas")
    grupo_analise = st.expander("Análise e Binarização")

    # 1. AJUSTES DE TOM
    with grupo_tom:
        st.caption("Brilho altera a intensidade; contraste separa tons; gama ajusta a iluminação.")
        
        if st.button("Preto & Branco", use_container_width=True):
            base = obter_base()
            resultado = pontuais.converter_para_cinza(base)
            registrar_nova_etapa("Escala de Cinza", resultado)
            st.rerun()

        v_brilho = st.slider("Brilho", -100, 100, 0, step=5)
        if st.button("Aplicar Brilho", use_container_width=True):
            base = obter_base()
            resultado = pontuais.ajustar_brilho(base, v_brilho)
            registrar_nova_etapa(f"Brilho ({v_brilho:+d})", resultado)
            st.rerun()

        v_contraste = st.slider("Contraste", 0.2, 2.5, 1.0, step=0.1)
        if st.button("Aplicar Contraste", use_container_width=True):
            base = obter_base()
            resultado = pontuais.ajustar_contraste(base, v_contraste)
            registrar_nova_etapa(f"Contraste ({v_contraste:.1f}x)", resultado)
            st.rerun()

        v_gama = st.slider("Gama", 0.1, 3.0, 1.0, step=0.1)
        if st.button("Aplicar Gama", use_container_width=True):
            base = obter_base()
            resultado = pontuais.ajustar_gama(base, v_gama)
            registrar_nova_etapa(f"Gama ({v_gama:.1f})", resultado)
            st.rerun()

        if st.button("Alongamento de Contraste", use_container_width=True):
            base = obter_base()
            resultado = pontuais.alongar_contraste(base)
            registrar_nova_etapa("Alongamento de Contraste", resultado)
            st.rerun()

    # 2. EFEITOS VISUAIS
    with grupo_efeitos:
        st.caption("Efeitos estilizados para modificação de cores.")
        if st.button("Negativo", use_container_width=True):
            base = obter_base()
            resultado = pontuais.aplicar_negativo(base)
            registrar_nova_etapa("Negativo", resultado)
            st.rerun()

        if st.button("Sépia", use_container_width=True):
            base = obter_base()
            resultado = pontuais.aplicar_sepia(base)
            registrar_nova_etapa("Sépia", resultado)
            st.rerun()

        v_niveis = st.slider("Níveis de Posterização", 2, 16, 4)
        if st.button("Aplicar Posterização", use_container_width=True):
            base = obter_base()
            resultado = pontuais.posterizar(base, v_niveis)
            registrar_nova_etapa(f"Posterização ({v_niveis} níveis)", resultado)
            st.rerun()

    # 3. FILTROS ESPACIAIS
    with grupo_filtros:
        st.caption("Filtros de suavização e nitidez.")
        tamanho_media = st.select_slider("Janela da Média", options=[3, 5, 7], value=3)
        if st.button("Suavização por Média", use_container_width=True):
            base = obter_base()
            resultado = espaciais.suavizar_media(base, tamanho_media)
            registrar_nova_etapa(f"Média ({tamanho_media}x{tamanho_media})", resultado)
            st.rerun()

        v_ruido = st.slider("Intensidade do Ruído", 5, 50, 25)
        if st.button("Adicionar Ruído Artificial", use_container_width=True):
            base = obter_base()
            resultado = espaciais.adicionar_ruido_gaussiano(base, v_ruido)
            registrar_nova_etapa(f"Ruído Gaussiano (σ={v_ruido})", resultado)
            st.rerun()

        sigma_gaussiano = st.slider("Sigma Gaussiano", 0.5, 3.0, 1.0, step=0.5)
        if st.button("Suavização Gaussiana", use_container_width=True):
            base = obter_base()
            resultado = espaciais.suavizar_gaussiano(base, sigma_gaussiano)
            registrar_nova_etapa(f"Gaussiano (σ={sigma_gaussiano:.1f})", resultado)
            st.rerun()

        intensidade_nitidez = st.slider("Intensidade Nitidez", 0.1, 2.0, 1.0, step=0.1)
        if st.button("Realçar Nitidez", use_container_width=True):
            base = obter_base()
            resultado = espaciais.realcar_nitidez(base, intensidade_nitidez)
            registrar_nova_etapa(f"Nitidez ({intensidade_nitidez:.1f})", resultado)
            st.rerun()

    # 4. DETECÇÃO DE BORDAS
    with grupo_bordas:
        st.caption("Filtros de gradiente para destacar contornos.")
        operador_borda = st.selectbox("Operador", ("Sobel", "Prewitt", "Laplaciano"))
        intensidade_borda = st.slider("Intensidade Bordas", 0.1, 3.0, 1.0, step=0.1)
        if st.button("Detectar Bordas", use_container_width=True):
            base = obter_base()
            detectores = {
                "Sobel": espaciais.detectar_sobel,
                "Prewitt": espaciais.detectar_prewitt,
                "Laplaciano": espaciais.detectar_laplaciano,
            }
            resultado = detectores[operador_borda](base, intensidade_borda)
            registrar_nova_etapa(f"Bordas: {operador_borda}", resultado)
            st.rerun()
            
    # 5. TRANSFORMAÇÕES GEOMÉTRICAS        
    with grupo_geometria:
        st.caption("Rotações, espelhamento, escala e translação.")
        sentido_rotacao = st.selectbox("Sentido Rotação 90°", ("Horário", "Anti-horário"))
        if st.button("Rotacionar 90°", use_container_width=True):
            base = obter_base()
            horario = sentido_rotacao == "Horário"
            resultado = geometricas.rotacionar_90(base, horario)
            desc = "horário" if horario else "anti-horário"
            registrar_nova_etapa(f"Rotação 90° ({desc})", resultado)
            st.rerun()

        if st.button("Espelhar Horizontalmente", use_container_width=True):
            base = obter_base()
            resultado = geometricas.espelhar_horizontal(base)
            registrar_nova_etapa("Espelhar H", resultado)
            st.rerun()

        if st.button("Espelhar Verticalmente", use_container_width=True):
            base = obter_base()
            resultado = geometricas.espelhar_vertical(base)
            registrar_nova_etapa("Espelhar V", resultado)
            st.rerun()

        escala = st.slider("Escala (%)", 25, 200, 100, step=5)
        if st.button("Redimensionar", use_container_width=True):
            base = obter_base()
            resultado = geometricas.redimensionar(base, escala)
            registrar_nova_etapa(f"Redimensionar ({escala}%)", resultado)
            st.rerun()

        v_angulo = st.slider("Ângulo de Rotação (°)", -180, 180, 0, step=5)
        if st.button("Aplicar Rotação", use_container_width=True):
            base = obter_base()
            resultado = geometricas.rotacionar_angulo(base, v_angulo)
            registrar_nova_etapa(f"Rotação ({v_angulo}°)", resultado)
            st.rerun()

        dx = st.number_input("Deslocamento X (pixels)", value=0, step=10)
        dy = st.number_input("Deslocamento Y (pixels)", value=0, step=10)
        if st.button("Aplicar Translação", use_container_width=True):
            base = obter_base()
            resultado = geometricas.transladar(base, dx, dy)
            registrar_nova_etapa(f"Translação (X:{dx}, Y:{dy})", resultado)
            st.rerun()
   
    # 6. ANÁLISE E BINARIZAÇÃO
    with grupo_analise:
        st.caption("Limiarização e equalização.")
        v_limiar = st.slider("Limiar de Binarização", 0, 255, 128)
        if st.button("Aplicar Binarização", use_container_width=True):
            base = obter_base()
            resultado = pontuais.binarizar(base, v_limiar)
            registrar_nova_etapa(f"Binarização ({v_limiar})", resultado)
            st.rerun()

        if st.button("Equalizar Histograma", use_container_width=True):
            base = obter_base()
            resultado = pontuais.equalizar_histograma(base)
            registrar_nova_etapa("Equalização", resultado)
            st.rerun()
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

        col_h, col_v = st.columns(2)
        with col_h:
            if st.button("Espelhar H", use_container_width=True):
                base = obter_base()
                resultado = geometricas.espelhar_horizontal(base)
                registrar_nova_etapa("Espelhar H", resultado)
                st.rerun()
        with col_v:
            if st.button("Espelhar V", use_container_width=True):
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

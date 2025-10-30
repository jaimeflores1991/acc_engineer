import streamlit as st
from recomendaciones import recomendacion_map

st.set_page_config(page_title="Ingeniero Virtual ACC", layout="wide")

# ----------------- ESTILO -----------------
st.markdown("""
    <style>
        .main-title {
            font-size: 36px;
            font-weight: 700;
            text-align: center;
            color: #00c3ff;
            margin-bottom: 20px;
        }
        .category-button > button {
            background-color: #1e1e1e !important;
            color: #00c3ff !important;
            border: 1px solid #00c3ff !important;
            border-radius: 10px !important;
            font-size: 18px !important;
            font-weight: 500 !important;
            padding: 10px !important;
            transition: 0.2s;
        }
        .category-button > button:hover {
            background-color: #00c3ff !important;
            color: #000 !important;
            transform: scale(1.03);
        }
        .reco-box {
            background-color: #111;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #333;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- SESIÓN -----------------
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "menu_principal"

if "recomendaciones" not in st.session_state:
    st.session_state.recomendaciones = []

# ----------------- MENÚ PRINCIPAL -----------------
if st.session_state.current_menu == "menu_principal":
    st.markdown('<div class="main-title">🧠 Ingeniero Virtual - Assetto Corsa Competizione</div>', unsafe_allow_html=True)
    st.write("Selecciona una categoría para obtener recomendaciones personalizadas:")

    categorias = [
        "Frenos",
        "Suspensión / Agarre Mecánico",
        "Amortiguadores",
        "Aerodinámica",
        "Electrónica",
        "Neumáticos",
        "Resumen / Exportar",
    ]

    cols = st.columns(3)
    for i, cat in enumerate(categorias):
        with cols[i % 3]:
            with st.container():
                st.markdown('<div class="category-button">', unsafe_allow_html=True)
                if st.button(cat, use_container_width=True):
                    st.session_state.current_menu = cat
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ----------------- SUBMENUS -----------------
else:
    st.title(f"{st.session_state.current_menu}")

    cat = st.session_state.current_menu
    opciones = []

    for k, v in recomendacion_map.items():
        path_str = str(v.get("path", ""))  # <- evita error si falta "path"
        if (
            (cat == "Frenos" and "brake" in path_str)
            or (cat == "Aerodinámica" and "aeroBalance" in path_str)
            or (cat == "Suspensión / Agarre Mecánico" and "mechanicalBalance" in path_str)
            or (cat == "Electrónica" and "electronics" in path_str)
            or (cat == "Amortiguadores" and "dampers" in path_str)
            or (cat == "Neumáticos" and ("tyres" in path_str or "alignment" in path_str))
        ):
            opciones.append(k)

    if not opciones:
        st.info("⚠️ No hay recomendaciones definidas para esta categoría aún.")
    else:
        for op in opciones:
            if st.button(op, use_container_width=True):
                if op not in st.session_state.recomendaciones:
                    st.session_state.recomendaciones.append(op)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Volver al menú principal"):
        st.session_state.current_menu = "menu_principal"
        st.rerun()

# ----------------- RESUMEN Y EXPORTACIÓN -----------------
if st.session_state.current_menu == "Resumen / Exportar":
    st.subheader("🧾 Resumen de recomendaciones seleccionadas")
    if not st.session_state.recomendaciones:
        st.write("No has seleccionado recomendaciones aún.")
    else:
        for rec in st.session_state.recomendaciones:
            data = recomendacion_map.get(rec, {})
            desc = data.get("desc", "Sin descripción disponible.")
            st.markdown(f"<div class='reco-box'><b>{rec}</b><br>{desc}</div>", unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Descargar recomendaciones",
        data="\n\n".join(
            [f"{r}: {recomendacion_map[r].get('desc', '')}" for r in st.session_state.recomendaciones]
        ),
        file_name="recomendaciones_ACC.txt",
    )

    if st.button("🔁 Reiniciar selección"):
        st.session_state.recomendaciones = []
        st.session_state.current_menu = "menu_principal"
        st.rerun()

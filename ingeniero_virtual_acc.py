import json
import streamlit as st
from recomendaciones import recomendacion_map

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="wide")

# --- ESTILO GENERAL ---
st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: 700;
    text-align: center;
    color: #00c3ff;
    margin-bottom: 25px;
}
.center {
    text-align: center;
}
.category-button > button {
    background-color: #1e1e1e !important;
    color: #00c3ff !important;
    border: 1px solid #00c3ff !important;
    border-radius: 12px !important;
    font-size: 18px !important;
    font-weight: 500 !important;
    padding: 12px !important;
    margin: 6px !important;
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

# --- SESIÓN ---
for key, default in {
    "setup_cargado": False,
    "setup_data": {},
    "current_menu": "inicio",
    "recomendaciones": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- INICIO ---
if st.session_state.current_menu == "inicio":
    st.markdown('<div class="main-title">🧠 Ingeniero de Pista - ACC</div>', unsafe_allow_html=True)
    st.write("Carga tu setup o continúa sin cargar para obtener recomendaciones generales.")

    setup_file = st.file_uploader("📂 Cargar setup (.json)", type=["json"])
    if setup_file:
        try:
            st.session_state.setup_data = json.load(setup_file)
            st.session_state.setup_cargado = True
            st.session_state.current_menu = "menu_principal"
            st.rerun()
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    col = st.columns(3)[1]
    with col:
        if st.button("➡️ Continuar sin cargar setup", use_container_width=True):
            st.session_state.setup_data = {}
            st.session_state.setup_cargado = False
            st.session_state.current_menu = "menu_principal"
            st.rerun()

# --- MENÚ PRINCIPAL ---
elif st.session_state.current_menu == "menu_principal":
    st.markdown('<div class="main-title">Menú principal</div>', unsafe_allow_html=True)
    if st.session_state.setup_cargado:
        st.success("✅ Setup cargado correctamente.")
    else:
        st.info("⚙️ Modo sin setup cargado.")

    categorias = [
        "Frenos",
        "Suspensión / Agarre Mecánico",
        "Amortiguadores",
        "Aerodinámica",
        "Electrónica",
        "Neumáticos",
        "Resumen / Exportar",
    ]

    st.markdown("<div class='center'>", unsafe_allow_html=True)
    for cat in categorias:
        st.markdown('<div class="category-button">', unsafe_allow_html=True)
        if st.button(cat, use_container_width=True, key=f"cat_{cat}"):
            st.session_state.current_menu = cat
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- SUBMENUS DE CATEGORÍAS ---
else:
    cat = st.session_state.current_menu
    st.markdown(f'<div class="main-title">{cat}</div>', unsafe_allow_html=True)

    # --- filtrar opciones seguras ---
    opciones = []
    for k, v in recomendacion_map.items():
        if not isinstance(v, dict):
            continue
        path = str(v.get("path", "")).lower()

        if (
            (cat == "Frenos" and "brake" in path)
            or (cat == "Aerodinámica" and "aero" in path)
            or (cat == "Suspensión / Agarre Mecánico" and "mechanical" in path)
            or (cat == "Electrónica" and "electronics" in path)
            or (cat == "Amortiguadores" and "damper" in path)
            or (cat == "Neumáticos" and ("tyre" in path or "alignment" in path))
        ):
            opciones.append(k)

    if not opciones:
        st.info("⚠️ No hay recomendaciones disponibles en esta categoría.")
    else:
        for op in opciones:
            if st.button(op, use_container_width=True, key=f"rec_{op}"):
                if op not in st.session_state.recomendaciones:
                    st.session_state.recomendaciones.append(op)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Volver al menú principal"):
            st.session_state.current_menu = "menu_principal"
            st.rerun()
    with col2:
        if st.button("🏠 Volver al inicio"):
            st.session_state.current_menu = "inicio"
            st.rerun()

# --- RESUMEN / EXPORTAR ---
if st.session_state.current_menu == "Resumen / Exportar":
    st.subheader("🧾 Resumen de recomendaciones seleccionadas")

    if not st.session_state.recomendaciones:
        st.write("No has seleccionado recomendaciones aún.")
    else:
        eliminar = []
        for rec in st.session_state.recomendaciones:
            data = recomendacion_map.get(rec, {})
            desc = data.get("desc", "Sin descripción.")
            col1, col2 = st.columns([8, 1])
            with col1:
                st.markdown(f"<div class='reco-box'><b>{rec}</b><br>{desc}</div>", unsafe_allow_html=True)
            with col2:
                if st.button("❌", key=f"del_{rec}"):
                    eliminar.append(rec)

        for rec in eliminar:
            st.session_state.recomendaciones.remove(rec)
            st.rerun()

        st.download_button(
            label="⬇️ Exportar seleccionadas",
            data="\n\n".join([f"{r}: {recomendacion_map[r].get('desc', '')}" for r in st.session_state.recomendaciones]),
            file_name="recomendaciones_ACC.txt",
        )

    if st.button("🔁 Reiniciar todo"):
        st.session_state.clear()
        st.rerun()

# ingeniero_virtual_acc.py
import streamlit as st
import json
from recomendaciones import RECOMENDACIONES, MENU_SIMPLIFICADO
import base64

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="centered")

# --- Inicialización de variables ---
if "page" not in st.session_state:
    st.session_state.page = "home"
if "setup" not in st.session_state:
    st.session_state.setup = None
if "applied" not in st.session_state:
    st.session_state.applied = []

# --- Funciones ---
def reset_app():
    st.session_state.page = "home"
    st.session_state.setup = None
    st.session_state.applied = []

def apply_recommendation(reco):
    st.session_state.applied.append(reco)
    st.toast(f"Aplicado: {reco['accion']} {reco['change']}{reco['unit']}")  # ventanita temporal

# 🔧 Mejorado para exportar con formato igual al original
def download_setup():
    if st.session_state.setup:
        data = json.dumps(
            st.session_state.setup,
            indent=2,
            separators=(',', ': '),
            ensure_ascii=False
        )
        b64 = base64.b64encode(data.encode()).decode()
        href = (
            f'<a href="data:file/json;base64,{b64}" '
            f'download="setup_modificado.json">Descargar setup</a>'
        )
        st.markdown(href, unsafe_allow_html=True)

# --- Home Page ---
if st.session_state.page == "home":
    st.title("Ingeniero de Pista ACC")
    st.write("Selecciona una opción para comenzar:")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Cargar setup (JSON)", type=["json"])
        if uploaded_file:
            try:
                st.session_state.setup = json.load(uploaded_file)
                st.session_state.page = "menu"
            except:
                st.error("Error al leer el setup")
    with col2:
        if st.button("Continuar sin cargar setup"):
            st.session_state.page = "menu"

# --- Menu Principal ---
elif st.session_state.page == "menu":
    st.title("Categorías")
    for category in MENU_SIMPLIFICADO.keys():
        if st.button(category):
            st.session_state.selected_category = category
            st.session_state.page = "submenu_sintomas"

    if st.button("Borrar todo y volver al Home"):
        reset_app()

# --- Submenu Síntomas ---
elif st.session_state.page == "submenu_sintomas":
    st.title(f"{st.session_state.selected_category}")
    sintomas = MENU_SIMPLIFICADO[st.session_state.selected_category]
    for sintoma in sintomas:
        if st.button(sintoma):
            st.session_state.selected_sintoma = sintoma
            st.session_state.page = "submenu_recomendaciones"

    st.write("---")
    if st.button("Volver al menú principal"):
        st.session_state.page = "menu"

# --- Submenu Recomendaciones ---
elif st.session_state.page == "submenu_recomendaciones":
    st.title(f"{st.session_state.selected_sintoma}")
    category = st.session_state.selected_category
    sintoma = st.session_state.selected_sintoma

    recomendaciones = RECOMENDACIONES[category][sintoma]  # Ajuste según categoría
    for reco in recomendaciones:
        if st.button(reco["accion"]):
            apply_recommendation(reco)

        st.write(f"*{reco.get('desc','')}*")  # descripción debajo del botón

    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Volver a síntomas"):
            st.session_state.page = "submenu_sintomas"
    with col2:
        if st.button("Volver al menú principal"):
            st.session_state.page = "menu"

# --- Resumen y aplicación de cambios ---
if st.session_state.applied:
    st.write("## Resumen de recomendaciones aplicadas:")
    for idx, reco in enumerate(st.session_state.applied):
        col1, col2 = st.columns([0.9,0.1])
        with col1:
            st.write(f"- {reco['accion']} ({reco['change']}{reco['unit']})")
        with col2:
            if st.button("X", key=f"del_{idx}"):
                st.session_state.applied.pop(idx)
                st.experimental_rerun()

    if st.session_state.setup:
        if st.button("Exportar setup modificado"):
            download_setup()
    else:
        if st.button("Aplicar cambios a nuevo setup"):
            st.session_state.page = "menu"

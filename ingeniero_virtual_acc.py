# ingeniero_virtual_acc.py
import streamlit as st
import json
from recomendaciones import RECOMENDACIONES

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="centered")

# Inicializar variables de sesión
if 'setup' not in st.session_state:
    st.session_state.setup = None
if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = 'home'
if 'selecciones' not in st.session_state:
    st.session_state.selecciones = []

# Funciones auxiliares
def reset_app():
    st.session_state.setup = None
    st.session_state.menu_actual = 'home'
    st.session_state.selecciones = []

def aplicar_recomendacion(reco):
    st.session_state.selecciones.append(reco)
    st.toast(f"{reco['accion']} aplicado")  # Ventanita informativa

def eliminar_recomendacion(idx):
    if 0 <= idx < len(st.session_state.selecciones):
        st.session_state.selecciones.pop(idx)

# --- HOME ---
if st.session_state.menu_actual == 'home':
    st.title("Ingeniero de Pista ACC")
    st.markdown("### Carga tu setup o continúa sin setup")
    
    # Cargar setup
    setup_file = st.file_uploader("Selecciona un archivo JSON de setup", type=["json"])
    if setup_file:
        try:
            st.session_state.setup = json.load(setup_file)
            st.success("Setup cargado correctamente")
        except Exception as e:
            st.error(f"Error leyendo el setup: {e}")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Continuar sin cargar setup"):
            st.session_state.menu_actual = 'menu_principal'
            st.experimental_rerun()
    with col2:
        if st.session_state.setup:
            if st.button("Continuar con setup cargado"):
                st.session_state.menu_actual = 'menu_principal'
                st.experimental_rerun()

# --- MENU PRINCIPAL ---
elif st.session_state.menu_actual == 'menu_principal':
    st.title("Categorías de ajustes")
    for cat in RECOMENDACIONES.keys():
        if st.button(cat):
            st.session_state.menu_actual = cat
            st.experimental_rerun()
    
    st.markdown("---")
    if st.button("Volver al Home"):
        reset_app()
        st.experimental_rerun()

# --- SUBMENUS ---
elif st.session_state.menu_actual in RECOMENDACIONES:
    categoria = st.session_state.menu_actual
    st.title(categoria)
    
    sintomas = RECOMENDACIONES[categoria]
    for sintoma, acciones in sintomas.items():
        st.markdown(f"**{sintoma}**")
        for i, reco in enumerate(acciones):
            if st.button(f"{reco['accion']} ({reco['change']} {reco['unit']})", key=f"{categoria}_{sintoma}_{i}"):
                aplicar_recomendacion(reco)
            st.markdown(f"*{reco['desc']}*")
        st.markdown("---")
    
    # Botón volver al menu principal
    if st.button("Volver al menú principal"):
        st.session_state.menu_actual = 'menu_principal'
        st.experimental_rerun()

# --- RESUMEN DE RECOMENDACIONES ---
if st.session_state.selecciones:
    st.markdown("## Resumen de recomendaciones aplicadas:")
    for idx, reco in enumerate(st.session_state.selecciones):
        col1, col2 = st.columns([8, 1])
        with col1:
            st.markdown(f"- {reco['accion']} ({reco['change']} {reco['unit']})")
        with col2:
            if st.button("X", key=f"elim_{idx}"):
                eliminar_recomendacion(idx)
                st.experimental_rerun()
    
    st.markdown("---")
    # Botón descargar JSON
    export_data = {
        "setup": st.session_state.setup,
        "recomendaciones": st.session_state.selecciones
    }
    export_json = json.dumps(export_data, indent=2)
    st.download_button(
        label="Descargar setup con recomendaciones",
        data=export_json,
        file_name="setup_recomendado.json",
        mime="application/json"
    )

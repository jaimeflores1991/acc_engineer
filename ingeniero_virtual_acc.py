import streamlit as st
import json
import time
from recomendaciones import RECOMENDACIONES, MENU_SIMPLIFICADO

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="wide")

# Inicialización de session_state
if "step" not in st.session_state:
    st.session_state.step = "home"
if "setup" not in st.session_state:
    st.session_state.setup = None
if "applied_recs" not in st.session_state:
    st.session_state.applied_recs = []
if "current_category" not in st.session_state:
    st.session_state.current_category = None
if "current_sintoma" not in st.session_state:
    st.session_state.current_sintoma = None

# Funciones auxiliares
def reset_all():
    st.session_state.step = "home"
    st.session_state.setup = None
    st.session_state.applied_recs = []
    st.session_state.current_category = None
    st.session_state.current_sintoma = None

def apply_recommendation(rec):
    st.session_state.applied_recs.append(rec)
    st.success(f"Recomendación aplicada: {rec['accion']}")
    time.sleep(1.5)

def remove_recommendation(idx):
    st.session_state.applied_recs.pop(idx)

# --- HOME ---
if st.session_state.step == "home":
    st.title("Ingeniero de Pista ACC")
    st.write("Seleccione una opción:")
    col1, col2 = st.columns(2)
    with col1:
        setup_file = st.file_uploader("Cargar archivo de setup", type=["json"])
        if setup_file is not None:
            try:
                st.session_state.setup = json.load(setup_file)
                st.success("Setup cargado correctamente.")
                st.session_state.step = "menu_principal"
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error leyendo el setup: {e}")
    with col2:
        if st.button("Continuar sin cargar setup"):
            st.session_state.step = "menu_principal"
            st.experimental_rerun()
    if st.button("Borrar todo y volver al home"):
        reset_all()
        st.experimental_rerun()

# --- MENU PRINCIPAL ---
elif st.session_state.step == "menu_principal":
    st.title("Categorías")
    st.write("Seleccione una categoría:")
    for cat in MENU_SIMPLIFICADO:
        if st.button(cat):
            st.session_state.current_category = cat
            st.session_state.step = "sintomas"
            st.experimental_rerun()
    if st.button("Borrar todo y volver al home"):
        reset_all()
        st.experimental_rerun()

# --- SUBMENU SINTOMAS ---
elif st.session_state.step == "sintomas":
    st.title(f"{st.session_state.current_category}")
    sintomas = MENU_SIMPLIFICADO[st.session_state.current_category]
    for sintoma in sintomas:
        if st.button(sintoma):
            st.session_state.current_sintoma = sintoma
            st.session_state.step = "recomendaciones"
            st.experimental_rerun()
    st.write("")
    if st.button("Volver al menú principal"):
        st.session_state.step = "menu_principal"
        st.experimental_rerun()
    if st.button("Borrar todo y volver al home"):
        reset_all()
        st.experimental_rerun()

# --- SUBMENU RECOMENDACIONES ---
elif st.session_state.step == "recomendaciones":
    st.title(f"Recomendaciones para: {st.session_state.current_sintoma}")
    recs = RECOMENDACIONES.get(st.session_state.current_category, {}).get(st.session_state.current_sintoma, [])
    for idx, rec in enumerate(recs):
        with st.expander(rec["accion"]):
            st.write(rec.get("desc",""))
            if st.button(f"Aplicar ({rec['change']}{rec['unit']})", key=f"apply_{idx}"):
                apply_recommendation(rec)
                st.experimental_rerun()
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Volver a síntomas"):
            st.session_state.step = "sintomas"
            st.experimental_rerun()
    with col2:
        if st.button("Volver al menú principal"):
            st.session_state.step = "menu_principal"
            st.experimental_rerun()
    if st.button("Borrar todo y volver al home"):
        reset_all()
        st.experimental_rerun()

# --- RESUMEN DE RECOMENDACIONES ---
if st.session_state.applied_recs:
    st.write("---")
    st.subheader("Resumen de recomendaciones aplicadas:")
    for idx, rec in enumerate(st.session_state.applied_recs):
        col1, col2 = st.columns([8,1])
        with col1:
            st.write(f"{rec['accion']} ({rec['change']}{rec['unit']})")
        with col2:
            if st.button("❌", key=f"del_{idx}"):
                remove_recommendation(idx)
                st.experimental_rerun()
    st.write("")
    if st.session_state.setup:
        if st.button("Exportar setup modificado"):
            st.download_button("Descargar setup modificado", json.dumps(st.session_state.setup, indent=4), "setup_modificado.json")
    if st.button("Borrar todo y volver al home"):
        reset_all()
        st.experimental_rerun()

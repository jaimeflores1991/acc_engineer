# ingeniero_virtual_acc.py
import streamlit as st
import json
from recomendaciones import RECOMENDACIONES

# Inicialización de estado
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "home"
if "setup" not in st.session_state:
    st.session_state.setup = None
if "recomendaciones_seleccionadas" not in st.session_state:
    st.session_state.recomendaciones_seleccionadas = []
if "categoria_actual" not in st.session_state:
    st.session_state.categoria_actual = None
if "sintoma_actual" not in st.session_state:
    st.session_state.sintoma_actual = None

# Funciones de navegación
def cargar_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            st.session_state.setup = json.load(uploaded_file)
        except Exception as e:
            st.error(f"Error leyendo el setup: {e}")
    st.session_state.pantalla = "menu_principal"

def continuar_sin_setup():
    st.session_state.setup = None
    st.session_state.pantalla = "menu_principal"

def entrar_categoria(cat):
    st.session_state.categoria_actual = cat
    st.session_state.pantalla = "sintomas"

def entrar_sintoma(sintoma):
    st.session_state.sintoma_actual = sintoma
    st.session_state.pantalla = "recomendaciones"

def volver_menu_principal():
    st.session_state.categoria_actual = None
    st.session_state.sintoma_actual = None
    st.session_state.pantalla = "menu_principal"

def agregar_recomendacion(rec):
    if rec not in st.session_state.recomendaciones_seleccionadas:
        st.session_state.recomendaciones_seleccionadas.append(rec)

def eliminar_recomendacion(idx):
    if 0 <= idx < len(st.session_state.recomendaciones_seleccionadas):
        st.session_state.recomendaciones_seleccionadas.pop(idx)

# Layout centrado
st.markdown("<h1 style='text-align: center;'>Ingeniero de Pista ACC</h1>", unsafe_allow_html=True)

# Función para mostrar resumen siempre
def mostrar_resumen():
    if st.session_state.recomendaciones_seleccionadas:
        st.markdown("<h4 style='text-align: center;'>Resumen de Recomendaciones Seleccionadas</h4>", unsafe_allow_html=True)
        for idx, rec in enumerate(st.session_state.recomendaciones_seleccionadas):
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"- {rec['accion']} ({rec['change']}{rec['unit']})")
            with col2:
                if st.button("❌", key=f"del_{idx}"):
                    eliminar_recomendacion(idx)
                    st.experimental_rerun()
        st.markdown("<br>", unsafe_allow_html=True)

# Pantallas
if st.session_state.pantalla == "home":
    st.write("")
    st.write("")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Cargar setup ACC (.json)", type=["json"])
    if uploaded_file:
        cargar_setup(uploaded_file)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continuar sin cargar setup", key="continuar", help="Puedes continuar sin setup, se usarán valores por defecto"):
        continuar_sin_setup()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.pantalla == "menu_principal":
    st.markdown("<h2 style='text-align: center;'>Categorías</h2>", unsafe_allow_html=True)
    for cat in RECOMENDACIONES.keys():
        if st.button(cat):
            entrar_categoria(cat)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Ver resumen de recomendaciones"):
        st.session_state.pantalla = "resumen"

elif st.session_state.pantalla == "sintomas":
    cat = st.session_state.categoria_actual
    st.markdown(f"<h3 style='text-align: center;'>{cat} - Selecciona síntoma</h3>", unsafe_allow_html=True)
    sintomas = list(RECOMENDACIONES[cat].keys())
    for sintoma in sintomas:
        if st.button(sintoma):
            entrar_sintoma(sintoma)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Volver al menú principal"):
        volver_menu_principal()
    st.markdown("<hr>", unsafe_allow_html=True)
    mostrar_resumen()

elif st.session_state.pantalla == "recomendaciones":
    cat = st.session_state.categoria_actual
    sintoma = st.session_state.sintoma_actual
    st.markdown(f"<h3 style='text-align: center;'>{cat} - {sintoma}</h3>", unsafe_allow_html=True)
    recs = RECOMENDACIONES[cat][sintoma]
    for i, r in enumerate(recs):
        if st.button(f"{r['accion']} ({r['change']}{r['unit']})", key=f"rec_{i}"):
            agregar_recomendacion(r)
        st.markdown(f"<div style='text-align: center; font-size: 0.9em; color: gray;'>{r['desc']}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Volver a síntomas"):
        st.session_state.pantalla = "sintomas"
        st.session_state.sintoma_actual = None
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Volver al menú principal"):
        volver_menu_principal()
    st.markdown("<hr>", unsafe_allow_html=True)
    mostrar_resumen()

elif st.session_state.pantalla == "resumen":
    st.markdown("<h2 style='text-align: center;'>Resumen de Recomendaciones</h2>", unsafe_allow_html=True)
    mostrar_resumen()
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Volver al menú principal"):
        volver_menu_principal()
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.recomendaciones_seleccionadas:
        # Exportar setup simulado
        if st.button("Exportar recomendaciones seleccionadas"):
            st.download_button(
                "Descargar JSON",
                data=json.dumps(st.session_state.recomendaciones_seleccionadas, indent=4),
                file_name="recomendaciones_export.json",
                mime="application/json"
            )

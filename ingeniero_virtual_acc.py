import streamlit as st
import json
from recomendaciones import RECOMENDACIONES

# -------------------------------
# Inicialización de estado
# -------------------------------
if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = 'home'

if 'setup' not in st.session_state:
    st.session_state.setup = None

if 'resumen' not in st.session_state:
    st.session_state.resumen = []

if 'categoria' not in st.session_state:
    st.session_state.categoria = None

# -------------------------------
# Funciones
# -------------------------------
def cargar_setup(archivo):
    try:
        data = json.load(archivo)
        st.session_state.setup = data
        st.session_state.menu_actual = 'menu_principal'
        st.session_state.categoria = None
        st.success("Setup cargado correctamente")
    except Exception as e:
        st.error(f"Error leyendo el setup: {e}")

def aplicar_accion(acc):
    st.session_state.resumen.append(acc)
    # Aquí podrías modificar directamente st.session_state.setup según acc['path'] y acc['change']
    st.toast(f"Acción aplicada: {acc['accion']}")  # Streamlit >=1.26.0 soporta st.toast

def borrar_resumen():
    st.session_state.resumen = []
    st.session_state.menu_actual = 'home'
    st.session_state.setup = None
    st.session_state.categoria = None

def descargar_setup():
    if st.session_state.setup:
        st.download_button(
            label="Descargar setup modificado",
            data=json.dumps(st.session_state.setup, indent=4),
            file_name="setup_modificado.json",
            mime="application/json"
        )

# -------------------------------
# Menú Home
# -------------------------------
if st.session_state.menu_actual == 'home':
    st.title("Ingeniero de Pista ACC")
    st.write("Carga un setup o continúa sin cargar")
    
    col1, col2 = st.columns([1,1])
    with col1:
        archivo = st.file_uploader("Cargar archivo JSON de setup", type=["json"])
        if archivo:
            cargar_setup(archivo)
    with col2:
        if st.button("Continuar sin cargar setup"):
            st.session_state.menu_actual = 'menu_principal'

# -------------------------------
# Menú principal
# -------------------------------
elif st.session_state.menu_actual == 'menu_principal' and st.session_state.categoria is None:
    st.title("Categorías de ajuste")
    for cat in RECOMENDACIONES.keys():
        if st.button(cat):
            st.session_state.categoria = cat

# -------------------------------
# Submenú de categoría
# -------------------------------
elif st.session_state.menu_actual == 'menu_principal' and st.session_state.categoria:
    cat = st.session_state.categoria
    st.title(f"{cat}")
    
    sintomas = RECOMENDACIONES[cat]
    for sintoma, acciones in sintomas.items():
        st.subheader(sintoma)
        for acc in acciones:
            if st.button(acc['accion'], key=f"{cat}_{sintoma}_{acc['accion']}"):
                aplicar_accion(acc)
            st.caption(acc.get('desc', ''))

    st.button("Volver al menú principal", on_click=lambda: st.session_state.update({'categoria': None}))

# -------------------------------
# Resumen de acciones
# -------------------------------
if st.session_state.resumen:
    st.markdown("### Resumen de recomendaciones aplicadas:")
    for i, acc in enumerate(st.session_state.resumen):
        col1, col2 = st.columns([6,1])
        with col1:
            st.write(f"- {acc['accion']} ({acc['change']} {acc['unit']})")
        with col2:
            if st.button("X", key=f"borrar_{i}"):
                st.session_state.resumen.pop(i)
                st.experimental_rerun = None  # ya no se usa, actualizar estado

    st.button("Borrar todo y volver al home", on_click=borrar_resumen)
    descargar_setup()

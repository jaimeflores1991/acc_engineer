# ingeniero_virtual_acc.py
import streamlit as st
import json
from recomendaciones import RECOMENDACIONES

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="centered")

# --- Funciones auxiliares ---
def cargar_setup(file):
    try:
        return json.load(file)
    except Exception as e:
        st.error(f"Error al cargar setup: {e}")
        return {}

def aplicar_recomendacion(setup, rec):
    """Aplica la recomendación al setup (simulado, solo para demo)"""
    current = setup
    try:
        for key in rec['path'][:-1]:
            current = current[key]
        idx = rec['path'][-1]
        if isinstance(idx, int):
            current[idx] += float(rec['change'])
        else:
            current[idx] += rec['change']
    except Exception:
        pass  # si falla, se ignora, solo demo
    return setup

# --- Estado de la app ---
if 'setup' not in st.session_state:
    st.session_state['setup'] = None
if 'resumen' not in st.session_state:
    st.session_state['resumen'] = []

# --- Home ---
if st.session_state['setup'] is None and 'home_done' not in st.session_state:
    st.title("Ingeniero de Pista ACC")
    st.markdown("Carga un setup o continua sin cargar.")
    col1, col2 = st.columns([1,1])
    with col1:
        uploaded_file = st.file_uploader("Cargar JSON de setup", type=["json"])
        if uploaded_file is not None:
            st.session_state['setup'] = cargar_setup(uploaded_file)
            st.session_state['home_done'] = True
            st.experimental_rerun()
    with col2:
        if st.button("Continuar sin setup", key="sin_setup"):
            st.session_state['setup'] = {}
            st.session_state['home_done'] = True
            st.experimental_rerun()
else:
    # --- Menu principal ---
    st.title("Categorías")
    categorias = list(RECOMENDACIONES.keys())
    for cat in categorias:
        if st.button(cat, key=f"cat_{cat}"):
            st.session_state['categoria'] = cat
            st.experimental_rerun()

    # --- Submenu síntomas ---
    if 'categoria' in st.session_state:
        cat = st.session_state['categoria']
        st.header(f"{cat} - Selecciona un síntoma")
        sintomas = RECOMENDACIONES[cat]
        for sintoma, acciones in sintomas.items():
            if st.button(sintoma, key=f"sint_{sintoma}"):
                st.session_state['sintoma'] = sintoma
                st.experimental_rerun()
        if st.button("Volver al menu principal"):
            st.session_state.pop('categoria')
            st.experimental_rerun()

    # --- Recomendaciones ---
    if 'sintoma' in st.session_state:
        sintoma = st.session_state['sintoma']
        cat = st.session_state['categoria']
        st.subheader(f"Recomendaciones para: {sintoma}")
        acciones = RECOMENDACIONES[cat][sintoma]
        for rec in acciones:
            label = f"{rec['accion']} ({rec['change']}{rec['unit']})"
            if st.button(label, key=f"rec_{rec['accion']}"):
                # Aplicar cambio al setup (simulado)
                st.session_state['setup'] = aplicar_recomendacion(st.session_state['setup'], rec)
                # Agregar al resumen
                st.session_state['resumen'].append(rec)
                st.success(f"Añadido: {rec['accion']}")
        if st.button("Volver al menu principal"):
            st.session_state.pop('sintoma')
            st.experimental_rerun()

    # --- Resumen ---
    st.sidebar.title("Resumen de cambios")
    if st.session_state['resumen']:
        for idx, rec in enumerate(st.session_state['resumen']):
            st.sidebar.write(f"{rec['accion']} ({rec['change']}{rec['unit']})")
            if st.sidebar.button("❌", key=f"del_{idx}"):
                st.session_state['resumen'].pop(idx)
                st.experimental_rerun()
        if st.sidebar.button("Exportar resumen"):
            export_data = json.dumps(st.session_state['resumen'], indent=2)
            st.sidebar.download_button("Descargar JSON", export_data, "resumen.json")
    else:
        st.sidebar.write("No hay cambios aplicados.")

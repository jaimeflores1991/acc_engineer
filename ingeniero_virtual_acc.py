import streamlit as st
import json
from recomendaciones import RECOMENDACIONES  # Tu archivo con mapa completo de recomendaciones

# --- Inicialización de estados ---
if "setup" not in st.session_state:
    st.session_state.setup = None
if "resumen" not in st.session_state:
    st.session_state.resumen = []
if "menu_actual" not in st.session_state:
    st.session_state.menu_actual = "home"
if "submenu_actual" not in st.session_state:
    st.session_state.submenu_actual = None

# --- Funciones ---
def cargar_setup(uploaded_file):
    try:
        st.session_state.setup = json.load(uploaded_file)
        st.success("Setup cargado correctamente!")
        st.session_state.menu_actual = "menu_principal"
    except Exception as e:
        st.error(f"Error al cargar setup: {e}")

def continuar_sin_setup():
    st.session_state.menu_actual = "menu_principal"

def aplicar_recomendacion(reco):
    """Agrega la recomendación al resumen si no está ya"""
    if reco not in st.session_state.resumen:
        st.session_state.resumen.append(reco)

def exportar_setup():
    if not st.session_state.setup:
        st.warning("Debes cargar un setup para exportar los cambios.")
        return
    # Aplicar cambios seleccionados
    setup_mod = st.session_state.setup.copy()
    for r in st.session_state.resumen:
        if "path" in r and "valor" in r:
            temp = setup_mod
            for p in r["path"][:-1]:
                if isinstance(p, int):
                    temp = temp[p]
                else:
                    temp = temp.get(p, {})
            # Último elemento
            key = r["path"][-1]
            temp[key] = r["valor"]
    st.download_button(
        "Descargar Setup Modificado",
        data=json.dumps(setup_mod, indent=2),
        file_name="setup_modificado.json"
    )

# --- Interfaz ---
st.title("Ingeniero de Pista ACC")
st.markdown("---")

if st.session_state.menu_actual == "home":
    # Botón de cargar setup
    uploaded_file = st.file_uploader("Carga un setup ACC (JSON)", type="json")
    if uploaded_file:
        cargar_setup(uploaded_file)
        st.experimental_rerun()

    # Botón continuar sin setup
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    if st.button("Continuar sin cargar setup"):
        continuar_sin_setup()
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.menu_actual == "menu_principal":
    st.subheader("Categorías")
    categorias = list(RECOMENDACIONES.keys())
    for cat in categorias:
        if st.button(cat):
            st.session_state.submenu_actual = cat
            st.session_state.menu_actual = "submenu"
            st.experimental_rerun()
    
    # Resumen general
    st.markdown("---")
    st.subheader("Resumen de Cambios")
    if st.session_state.resumen:
        for idx, r in enumerate(st.session_state.resumen):
            st.markdown(f"**{r['titulo']}**: {r.get('descripcion','')}")
            if st.button(f"Eliminar X", key=f"elim_{idx}"):
                st.session_state.resumen.pop(idx)
                st.experimental_rerun()
    else:
        st.info("No hay cambios aplicados aún.")

    # Exportar
    if st.session_state.setup:
        st.markdown("---")
        if st.button("Exportar Setup Modificado"):
            exportar_setup()

elif st.session_state.menu_actual == "submenu":
    cat = st.session_state.submenu_actual
    st.subheader(cat)
    opciones = RECOMENDACIONES[cat]

    for op in opciones:
        desc = op.get("descripcion","")
        # Botón de recomendación
        if st.button(op["titulo"]):
            aplicar_recomendacion(op)
            st.success(f"Recomendación '{op['titulo']}' agregada al resumen")
        if desc:
            st.markdown(f"*{desc}*")

    # Botón volver al menu principal
    st.markdown("---")
    if st.button("Volver al menú principal"):
        st.session_state.menu_actual = "menu_principal"
        st.session_state.submenu_actual = None
        st.experimental_rerun()

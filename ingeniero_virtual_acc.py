import streamlit as st
import json
from recomendaciones import mapa_recomendaciones

# Inicializar sesión
if "menu_actual" not in st.session_state:
    st.session_state.menu_actual = "home"
if "setup" not in st.session_state:
    st.session_state.setup = None
if "resumen" not in st.session_state:
    st.session_state.resumen = []

# Función para agregar recomendación al resumen
def agregar_recomendacion(rec):
    if rec not in st.session_state.resumen:
        st.session_state.resumen.append(rec)

# Función para eliminar recomendación del resumen
def eliminar_recomendacion(idx):
    st.session_state.resumen.pop(idx)

# Función para exportar JSON
def exportar_setup():
    if st.session_state.setup is None:
        st.warning("Debes cargar un setup para exportar cambios")
        return
    setup_mod = st.session_state.setup.copy()
    for rec in st.session_state.resumen:
        path = rec["path"]
        valor = rec["valor_aplicar"]
        # Aplicar al setup (solo si existe)
        temp = setup_mod
        for p in path[:-1]:
            temp = temp[int(p)] if isinstance(temp, list) else temp.get(p, {})
        last = path[-1]
        if isinstance(temp, dict) and last in temp:
            temp[last] = valor
    st.download_button(
        "Descargar setup modificado",
        data=json.dumps(setup_mod, indent=2),
        file_name="setup_modificado.json"
    )

# --- Home ---
if st.session_state.menu_actual == "home":
    st.title("Ingeniero de Pista ACC")
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Carga un setup ACC (JSON)", type="json")
    if uploaded_file is not None:
        try:
            st.session_state.setup = json.load(uploaded_file)
            st.success("Setup cargado correctamente!")
            st.session_state.menu_actual = "menu_principal"
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error al cargar setup: {e}")
    if st.button("Continuar sin cargar setup", key="continuar_home"):
        st.session_state.menu_actual = "menu_principal"
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- Menú principal ---
elif st.session_state.menu_actual == "menu_principal":
    st.header("Categorías")
    for cat in mapa_recomendaciones.keys():
        if st.button(cat):
            st.session_state.menu_actual = cat
            st.experimental_rerun()
    # Mostrar resumen y exportar
    if st.session_state.resumen:
        st.subheader("Resumen de recomendaciones")
        for idx, rec in enumerate(st.session_state.resumen):
            col1, col2, col3 = st.columns([6,1,2])
            with col1:
                st.write(f"{rec['titulo']}: {rec['descripcion']}")
            with col2:
                if st.button("X", key=f"eliminar_{idx}"):
                    eliminar_recomendacion(idx)
                    st.experimental_rerun()
            with col3:
                st.write(f"Aplicar: {rec['valor_aplicar']}")
        exportar_setup()

# --- Submenús ---
else:
    st.header(st.session_state.menu_actual)
    sintomas = mapa_recomendaciones.get(st.session_state.menu_actual, [])
    for rec in sintomas:
        if st.button(rec["titulo"]):
            agregar_recomendacion(rec)
    st.button("Volver al menú principal", on_click=lambda: st.session_state.update({"menu_actual":"menu_principal"}))

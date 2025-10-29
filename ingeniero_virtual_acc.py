import streamlit as st
import json
from recomendaciones import recomendacion_map
import copy

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="centered")

# ----------------- FUNCIONES -----------------

def cargar_setup(file):
    try:
        return json.load(file)
    except:
        st.error("Error al cargar JSON.")
        return None

def aplicar_cambio(setup, cambio):
    """
    Aplica un cambio del mapa de recomendaciones al setup.
    """
    if isinstance(cambio, list):
        # Si hay varios cambios en la recomendación
        for c in cambio:
            aplicar_cambio(setup, c)
        return

    path = cambio["path"]
    valor = cambio["change"]
    temp = setup
    for p in path[:-1]:
        temp = temp[p]
    key = path[-1]

    if isinstance(temp[key], list):
        # Si es lista (neumáticos u otros), se modifica cada valor
        for i in range(len(temp[key])):
            if valor.startswith('+') or valor.startswith('-'):
                temp[key][i] += float(valor)
            else:
                temp[key][i] = float(valor)
    else:
        if valor.startswith('+') or valor.startswith('-'):
            temp[key] += float(valor)
        else:
            temp[key] = float(valor)

# ----------------- ESTADO -----------------

if "setup" not in st.session_state:
    st.session_state.setup = None
if "recomendaciones" not in st.session_state:
    st.session_state.recomendaciones = []
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "home"

# ----------------- HOME -----------------

if st.session_state.current_menu == "home":
    st.title("Ingeniero de Pista ACC")
    st.subheader("Cargar setup ACC")
    uploaded_file = st.file_uploader("Selecciona un archivo JSON de setup", type="json")
    
    if uploaded_file:
        st.session_state.setup = cargar_setup(uploaded_file)
        st.session_state.current_menu = "menu_principal"
        st.experimental_rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align:center;'>
        <button style='width:200px;height:50px;font-size:18px;' onclick="window.streamlitClose()">Continuar sin cargar setup</button>
        </div>
        """, unsafe_allow_html=True
    )
    # Alternativa funcional de Streamlit
    if st.button("Continuar sin cargar setup", key="sin_setup"):
        st.session_state.setup = None
        st.session_state.current_menu = "menu_principal"
        st.experimental_rerun()

# ----------------- MENU PRINCIPAL -----------------

elif st.session_state.current_menu == "menu_principal":
    st.title("Categorías de Ajustes")
    st.markdown("<br>", unsafe_allow_html=True)

    categorias = [
        "Frenos",
        "Aerodinámica",
        "Suspensión / Agarre Mecánico",
        "Electrónica",
        "Amortiguadores",
        "Neumáticos"
    ]

    for cat in categorias:
        if st.button(cat, key=cat):
            st.session_state.current_menu = cat
            st.experimental_rerun()

# ----------------- SUBMENUS -----------------

else:
    st.title(f"{st.session_state.current_menu}")

    # Filtrar recomendaciones por categoría
    cat = st.session_state.current_menu
    opciones = []
    for k, v in recomendacion_map.items():
        if (cat == "Frenos" and "brake" in str(v["path"])) \
            or (cat == "Aerodinámica" and "aeroBalance" in str(v["path"])) \
            or (cat == "Suspensión / Agarre Mecánico" and "mechanicalBalance" in str(v["path"])) \
            or (cat == "Electrónica" and "electronics" in str(v["path"])) \
            or (cat == "Amortiguadores" and "dampers" in str(v["path"])) \
            or (cat == "Neumáticos" and ("tyres" in str(v["path"]) or "alignment" in str(v["path"]))):
            opciones.append(k)

    for op in opciones:
        if st.button(op):
            if op not in st.session_state.recomendaciones:
                st.session_state.recomendaciones.append(op)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Volver al menú principal"):
        st.session_state.current_menu = "menu_principal"
        st.experimental_rerun()

# ----------------- RESUMEN Y EXPORTACIÓN -----------------

if st.session_state.recomendaciones:
    st.markdown("---")
    st.subheader("Resumen de Recomendaciones")

    for r in st.session_state.recomendaciones:
        col1, col2 = st.columns([8,1])
        with col1:
            st.write(r)
        with col2:
            if st.button("X", key=f"del_{r}"):
                st.session_state.recomendaciones.remove(r)
                st.experimental_rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.setup is not None:
        if st.button("Exportar setup modificado"):
            setup_mod = copy.deepcopy(st.session_state.setup)
            for r in st.session_state.recomendaciones:
                aplicar_cambio(setup_mod, recomendacion_map[r])
            # Guardar JSON
            with open("setup_modificado.json", "w") as f:
                json.dump(setup_mod, f, indent=4)
            st.success("Setup exportado como setup_modificado.json")
    else:
        st.info("Para exportar debes cargar un setup primero.")

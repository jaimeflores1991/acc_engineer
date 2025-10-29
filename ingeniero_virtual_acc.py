import streamlit as st
import json
import copy

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="centered")

# ----------------------------------
# Funciones auxiliares
# ----------------------------------
def load_setup(file):
    try:
        return json.load(file)
    except:
        st.error("Archivo inválido")
        return None

def generar_recomendacion(param_name, valor_actual=None):
    if valor_actual is None:
        return f"Incrementar {param_name} 1 punto"
    else:
        return f"Incrementar {param_name} de {valor_actual} → {valor_actual+1}"

# ----------------------------------
# Estado inicial
# ----------------------------------
if "setup" not in st.session_state:
    st.session_state.setup = None
if "mostrar_menu" not in st.session_state:
    st.session_state.mostrar_menu = False
if "menu_seleccionado" not in st.session_state:
    st.session_state.menu_seleccionado = None
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "inicio"  # inicio o submenú
if "recomendaciones" not in st.session_state:
    st.session_state.recomendaciones = []

# ----------------------------------
# Título
# ----------------------------------
st.title("Ingeniero de Pista ACC")

# ----------------------------------
# Página inicio: cargar setup o continuar sin setup
# ----------------------------------
if st.session_state.pagina_actual == "inicio":
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    archivo_setup = st.file_uploader("Cargar archivo de setup", type=["json"])
    if archivo_setup:
        st.session_state.setup = load_setup(archivo_setup)
        st.session_state.mostrar_menu = True
        st.session_state.pagina_actual = "menu_principal"
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continuar sin cargar setup", key="continuar_setup", help="Entrar al ingeniero sin setup"):
        st.session_state.mostrar_menu = True
        st.session_state.pagina_actual = "menu_principal"
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------
# Menú principal (botones cuadrados, grid)
# ----------------------------------
if st.session_state.pagina_actual == "menu_principal" and st.session_state.mostrar_menu:
    st.subheader("Menú principal")
    menu = ["Frenos", "Aerodinámica", "Suspensión", "Electrónica", "Neumáticos", "Amortiguadores"]
    
    # Grid responsive con 3 columnas aprox
    cols = st.columns(3)
    for i, categoria in enumerate(menu):
        with cols[i % 3]:
            if st.button(categoria, key=f"menu_{categoria}", 
                         help=f"Abrir menú {categoria}", 
                         args=None):
                st.session_state.menu_seleccionado = categoria
                st.session_state.pagina_actual = "submenu"

# ----------------------------------
# Submenú
# ----------------------------------
if st.session_state.pagina_actual == "submenu":
    categoria = st.session_state.menu_seleccionado
    st.subheader(f"{categoria}")
    
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    
    # Ejemplo de síntomas por categoría
    if categoria == "Frenos":
        sintomas = ["No se detiene a tiempo", "Se detiene muy pronto", "Patina cuando freno"]
    elif categoria == "Aerodinámica":
        sintomas = ["Voy muy lento en rectas", "Patino en curvas rápidas", "El auto no gira en curvas"]
    else:
        sintomas = ["Opción 1", "Opción 2"]  # placeholder

    # Botones de síntomas
    for s in sintomas:
        if st.button(s, key=f"{categoria}_{s}"):
            rec = generar_recomendacion(s)
            st.session_state.recomendaciones.append(rec)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botón volver al menú principal
    if st.button("Volver al menú principal"):
        st.session_state.pagina_actual = "menu_principal"
        st.session_state.menu_seleccionado = None

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------
# Resumen de recomendaciones
# ----------------------------------
if st.session_state.recomendaciones:
    st.header("Resumen de recomendaciones")
    for i, rec in enumerate(st.session_state.recomendaciones):
        st.write(f"{i+1}. {rec}")

# ----------------------------------
# Exportar setup (solo si hay setup cargado y estamos en submenú)
# ----------------------------------
if st.session_state.pagina_actual == "submenu" and st.session_state.setup:
    if st.button("Exportar setup modificado"):
        setup_mod = copy.deepcopy(st.session_state.setup)
        with open("setup_modificado.json", "w") as f:
            json.dump(setup_mod, f, indent=2)
        st.success("Setup exportado como setup_modificado.json")

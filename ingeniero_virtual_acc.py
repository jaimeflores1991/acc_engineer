# ingeniero_virtual_acc_centrado.py
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

def set_valor_json(d, path, valor):
    temp = d
    for i, p in enumerate(path):
        if i == len(path)-1:
            if isinstance(temp, list) and p.isdigit():
                temp[int(p)] = valor
            else:
                temp[p] = valor
        else:
            temp = temp[int(p)] if p.isdigit() else temp.get(p, {})

def generar_recomendacion(param_name, valor_actual=None):
    if valor_actual is None:
        texto = f"Incrementar {param_name} 1 punto"
    else:
        texto = f"Incrementar {param_name} de {valor_actual} → {valor_actual+1}"
    return texto

# ----------------------------------
# Estado inicial
# ----------------------------------
if "setup" not in st.session_state:
    st.session_state.setup = None
if "recomendaciones" not in st.session_state:
    st.session_state.recomendaciones = []
if "mostrar_menu" not in st.session_state:
    st.session_state.mostrar_menu = False
if "menu_seleccionado" not in st.session_state:
    st.session_state.menu_seleccionado = None

# ----------------------------------
# Título y carga inicial centrada
# ----------------------------------
st.title("Ingeniero de Pista ACC", anchor=None)

st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
archivo_setup = st.file_uploader("Cargar archivo de setup", type=["json"])
if archivo_setup:
    st.session_state.setup = load_setup(archivo_setup)
    st.session_state.mostrar_menu = True

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Continuar sin cargar setup", key="continuar_setup"):
    st.session_state.mostrar_menu = True
st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------
# Menú principal en pantalla principal
# ----------------------------------
if st.session_state.mostrar_menu:
    st.subheader("Menú principal")
    menu = [
        "Frenos",
        "Aerodinámica",
        "Suspensión",
        "Electrónica",
        "Neumáticos",
        "Amortiguadores"
    ]

    # Mostrar cada menú como botón centrado
    for categoria in menu:
        if st.button(categoria, key=f"menu_{categoria}"):
            st.session_state.menu_seleccionado = categoria

# ----------------------------------
# Funciones de síntomas (ejemplo)
# ----------------------------------
def mostrar_sintomas_frenos():
    st.write("### Frenos")
    if st.button("No se detiene a tiempo", key="freno1"):
        rec = generar_recomendacion("presión de frenos", 50 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)
    if st.button("Se detiene muy pronto", key="freno2"):
        rec = generar_recomendacion("presión de frenos", 50 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)
    if st.button("Patina cuando freno", key="freno3"):
        rec = generar_recomendacion("presión freno delantero", 50 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)

def mostrar_sintomas_aero():
    st.write("### Aerodinámica")
    if st.button("Voy muy lento en rectas", key="aero1"):
        rec = generar_recomendacion("carga aerodinámica delantera", 5 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)
    if st.button("Patino en curvas rápidas", key="aero2"):
        rec = generar_recomendacion("carga aerodinámica trasera", 5 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)
    if st.button("El auto no gira en curvas", key="aero3"):
        rec = generar_recomendacion("carga aerodinámica delantera", 5 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)

# ----------------------------------
# Mostrar síntomas según menú seleccionado
# ----------------------------------
if st.session_state.menu_seleccionado:
    categoria = st.session_state.menu_seleccionado
    if categoria == "Frenos":
        mostrar_sintomas_frenos()
    elif categoria == "Aerodinámica":
        mostrar_sintomas_aero()
    # Aquí agregarías Suspensión, Electrónica, Neumáticos, Amortiguadores

# ----------------------------------
# Resumen de recomendaciones
# ----------------------------------
if st.session_state.recomendaciones:
    st.header("Resumen de recomendaciones")
    for i, rec in enumerate(st.session_state.recomendaciones):
        st.write(f"{i+1}. {rec}")

# ----------------------------------
# Exportar setup solo si no estamos en el menú inicial
# ----------------------------------
if st.session_state.menu_seleccionado and st.session_state.menu_seleccionado != "Frenos":
    if st.button("Exportar setup modificado", key="exportar"):
        if st.session_state.setup is None:
            st.warning("Debes cargar un setup antes de exportar")
        else:
            setup_mod = copy.deepcopy(st.session_state.setup)
            # Aplicar cambios acumulados
            with open("setup_modificado.json", "w") as f:
                json.dump(setup_mod, f, indent=2)
            st.success("Setup exportado como setup_modificado.json")

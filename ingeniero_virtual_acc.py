# ingeniero_virtual_acc_main.py
import streamlit as st
import json
import copy

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="wide")

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

# ----------------------------------
# Título y carga inicial
# ----------------------------------
st.title("Ingeniero de Pista ACC")

col1, col2 = st.columns(2)
with col1:
    archivo_setup = st.file_uploader("Cargar archivo de setup", type=["json"])
    if archivo_setup:
        st.session_state.setup = load_setup(archivo_setup)
        st.session_state.mostrar_menu = True

with col2:
    if st.button("Continuar sin cargar setup"):
        st.session_state.mostrar_menu = True

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

    # Cada menú como botón
    for categoria in menu:
        if st.button(categoria):
            st.session_state.menu_seleccionado = categoria

# ----------------------------------
# Funciones de síntomas (ejemplo)
# ----------------------------------
def mostrar_sintomas_frenos():
    st.write("### Frenos")
    if st.button("No se detiene a tiempo"):
        rec = generar_recomendacion("presión de frenos", 50 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)
    if st.button("Se detiene muy pronto"):
        rec = generar_recomendacion("presión de frenos", 50 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)
    if st.button("Patina cuando freno"):
        rec = generar_recomendacion("presión freno delantero", 50 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)

def mostrar_sintomas_aero():
    st.write("### Aerodinámica")
    if st.button("Voy muy lento en rectas"):
        rec = generar_recomendacion("carga aerodinámica delantera", 5 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)
    if st.button("Patino en curvas rápidas"):
        rec = generar_recomendacion("carga aerodinámica trasera", 5 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)
    if st.button("El auto no gira en curvas"):
        rec = generar_recomendacion("carga aerodinámica delantera", 5 if st.session_state.setup else None)
        st.session_state.recomendaciones.append(rec)

# ----------------------------------
# Mostrar síntomas según menú seleccionado
# ----------------------------------
if "menu_seleccionado" in st.session_state:
    categoria = st.session_state.menu_seleccionado
    if categoria == "Frenos":
        mostrar_sintomas_frenos()
    elif categoria == "Aerodinámica":
        mostrar_sintomas_aero()
    # Aquí agregarías las demás categorías: Suspensión, Electrónica, Neumáticos, Amortiguadores

# ----------------------------------
# Resumen de recomendaciones
# ----------------------------------
st.header("Resumen de recomendaciones")
for i, rec in enumerate(st.session_state.recomendaciones):
    st.write(f"{i+1}. {rec}")

# ----------------------------------
# Exportar setup
# ----------------------------------
if st.button("Exportar setup modificado"):
    if st.session_state.setup is None:
        st.warning("Debes cargar un setup antes de exportar")
    else:
        setup_mod = copy.deepcopy(st.session_state.setup)
        # Aquí se aplicarían los cambios acumulados
        with open("setup_modificado.json", "w") as f:
            json.dump(setup_mod, f, indent=2)
        st.success("Setup exportado como setup_modificado.json")

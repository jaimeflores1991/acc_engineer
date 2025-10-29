# ingeniero_virtual_acc.py
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
    """Actualizar valor en JSON según path tipo 'advancedSetup.aeroBalance.rideHeight.0'"""
    temp = d
    for i, p in enumerate(path):
        if i == len(path)-1:
            if isinstance(temp, list) and p.isdigit():
                temp[int(p)] = valor
            else:
                temp[p] = valor
        else:
            temp = temp[int(p)] if p.isdigit() else temp.get(p, {})

def get_valor_json(d, path):
    """Obtener valor desde JSON según path"""
    temp = d
    for p in path:
        temp = temp[int(p)] if isinstance(temp, list) or p.isdigit() else temp.get(p, None)
        if temp is None:
            return None
    return temp

def generar_recomendacion(param_name, valor_actual=None):
    """Genera recomendación amigable"""
    texto = ""
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

if "historial" not in st.session_state:
    st.session_state.historial = []

# ----------------------------------
# Carga de setup
# ----------------------------------
st.title("Ingeniero de Pista ACC")

col1, col2 = st.columns(2)
with col1:
    archivo_setup = st.file_uploader("Cargar archivo de setup", type=["json"])
    if archivo_setup:
        st.session_state.setup = load_setup(archivo_setup)

with col2:
    if st.button("Continuar sin cargar setup"):
        st.session_state.setup = None

# ----------------------------------
# Menú principal
# ----------------------------------
st.sidebar.header("Menú principal")
menu_principal = st.sidebar.radio("Categorías", [
    "Frenos", "Aerodinámica", "Suspensión", "Electrónica", "Neumáticos", "Amortiguadores"
])

# ----------------------------------
# Síntomas y recomendaciones
# ----------------------------------
def mostrar_sintomas_frenos():
    st.sidebar.subheader("Frenos")
    opciones = [
        "No se detiene a tiempo",
        "Se detiene muy pronto",
        "Patina cuando freno"
    ]
    sintoma = st.sidebar.radio("Selecciona síntoma", opciones)
    if sintoma:
        if sintoma == "No se detiene a tiempo":
            if st.button("Subir presión de frenos"):
                val = 50  # valor ejemplo
                rec = generar_recomendacion("presión de frenos", val)
                st.session_state.recomendaciones.append(rec)
        elif sintoma == "Se detiene muy pronto":
            if st.button("Bajar presión de frenos"):
                val = 50
                rec = generar_recomendacion("presión de frenos", val-5)
                st.session_state.recomendaciones.append(rec)
        elif sintoma == "Patina cuando freno":
            if st.button("Delantero: reducir presión"):
                val = 50
                rec = generar_recomendacion("presión de freno delantero", val)
                st.session_state.recomendaciones.append(rec)

def mostrar_sintomas_aero():
    st.sidebar.subheader("Aerodinámica")
    opciones = [
        "Voy muy lento en las rectas",
        "Patino en curvas rápidas",
        "El auto no gira en curvas"
    ]
    sintoma = st.sidebar.radio("Selecciona síntoma", opciones)
    if sintoma:
        if sintoma == "Voy muy lento en las rectas":
            if st.button("Reducir carga delantera"):
                val = 5
                rec = generar_recomendacion("carga aerodinámica delantera", val)
                st.session_state.recomendaciones.append(rec)
            if st.button("Reducir carga trasera"):
                val = 5
                rec = generar_recomendacion("carga aerodinámica trasera", val)
                st.session_state.recomendaciones.append(rec)
        elif sintoma == "Patino en curvas rápidas":
            if st.button("Aumentar carga trasera"):
                val = 5
                rec = generar_recomendacion("carga aerodinámica trasera", val)
                st.session_state.recomendaciones.append(rec)

def mostrar_sintomas_suspension():
    st.sidebar.subheader("Suspensión / Agarre mecánico")
    opciones = [
        "El auto no gira en curvas",
        "El auto gira demasiado",
        "Neumáticos se desgastan"
    ]
    sintoma = st.sidebar.radio("Selecciona síntoma", opciones)
    if sintoma:
        if sintoma == "El auto no gira en curvas":
            if st.button("Aumentar rigidez delantera"):
                rec = generar_recomendacion("rigidez delantera", 3)
                st.session_state.recomendaciones.append(rec)
            if st.button("Bajar altura delantera"):
                rec = generar_recomendacion("altura delantera", 2)
                st.session_state.recomendaciones.append(rec)
        elif sintoma == "El auto gira demasiado":
            if st.button("Suavizar barra estabilizadora delantera"):
                rec = generar_recomendacion("barra estabilizadora delantera", 3)
                st.session_state.recomendaciones.append(rec)
        elif sintoma == "Neumáticos se desgastan":
            if st.button("Aumentar rigidez delantera"):
                rec = generar_recomendacion("rigidez delantera", 3)
                st.session_state.recomendaciones.append(rec)

def mostrar_sintomas_electronica():
    st.sidebar.subheader("Electrónica")
    opciones = [
        "No acelero suficiente / no llego a velocidad máxima"
    ]
    sintoma = st.sidebar.radio("Selecciona síntoma", opciones)
    if sintoma:
        if st.button("Ajustar TC"):
            rec = generar_recomendacion("control de tracción", 5)
            st.session_state.recomendaciones.append(rec)
        if st.button("Ajustar ABS"):
            rec = generar_recomendacion("ABS", 5)
            st.session_state.recomendaciones.append(rec)

def mostrar_sintomas_neumaticos():
    st.sidebar.subheader("Neumáticos")
    if st.button("Ajustar presión del neumático delantero izquierdo"):
        rec = generar_recomendacion("PSI del. izq.", 28)
        st.session_state.recomendaciones.append(rec)

def mostrar_sintomas_amortiguadores():
    st.sidebar.subheader("Amortiguadores")
    if st.button("Ajustar compresión del delantero izquierdo"):
        rec = generar_recomendacion("compresión delantero izq.", 20)
        st.session_state.recomendaciones.append(rec)

# ----------------------------------
# Llamada a menú
# ----------------------------------
if menu_principal == "Frenos":
    mostrar_sintomas_frenos()
elif menu_principal == "Aerodinámica":
    mostrar_sintomas_aero()
elif menu_principal == "Suspensión":
    mostrar_sintomas_suspension()
elif menu_principal == "Electrónica":
    mostrar_sintomas_electronica()
elif menu_principal == "Neumáticos":
    mostrar_sintomas_neumaticos()
elif menu_principal == "Amortiguadores":
    mostrar_sintomas_amortiguadores()

# ----------------------------------
# Resumen acumulativo
# ----------------------------------
st.header("Resumen de recomendaciones")
for i, rec in enumerate(st.session_state.recomendaciones):
    st.write(f"{i+1}. {rec}")

# ----------------------------------
# Exportar cambios
# ----------------------------------
if st.button("Exportar setup modificado"):
    if st.session_state.setup is None:
        st.warning("Debes cargar un setup antes de exportar")
    else:
        setup_mod = copy.deepcopy(st.session_state.setup)
        # Aquí aplicarías las modificaciones acumuladas
        # Por ahora solo guardamos el mismo setup para prueba
        with open("setup_modificado.json", "w") as f:
            json.dump(setup_mod, f, indent=2)
        st.success("Setup exportado como setup_modificado.json")

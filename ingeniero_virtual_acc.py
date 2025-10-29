import streamlit as st
import json
import copy

st.set_page_config(page_title="Ingeniero Virtual ACC", layout="wide")
st.title("🏎️ Ingeniero Virtual ACC")

# --- Funciones helper ---
def get_valor_json(data, path):
    temp = data
    for p in path:
        if p.isdigit():
            temp = temp[int(p)]
        else:
            temp = temp.get(p)
            if temp is None:
                return None
    return temp

def set_valor_json(data, path, valor):
    temp = data
    for i, p in enumerate(path[:-1]):
        if p.isdigit():
            p = int(p)
            while len(temp) <= p:
                temp.append({})
            temp = temp[p]
        else:
            if p not in temp:
                temp[p] = {}
            temp = temp[p]
    ult = path[-1]
    if ult.isdigit():
        ult = int(ult)
        while len(temp) <= ult:
            temp.append(None)
        temp[ult] = valor
    else:
        temp[ult] = valor

# --- Mapeo técnico -> descripción amigable ---
param_desc = {
    "advancedSetup.aeroBalance.rearWing": "Alerón trasero",
    "advancedSetup.aeroBalance.rideHeight[0]": "Altura delantera",
    "advancedSetup.aeroBalance.rideHeight[1]": "Altura trasera",
    "advancedSetup.mechanicalBalance.aRBFront": "Barra estabilizadora delantera",
    "advancedSetup.mechanicalBalance.aRBRear": "Barra estabilizadora trasera",
    "advancedSetup.dampers.reboundSlow[2]": "Amortiguador trasero lento derecho",
    "advancedSetup.dampers.reboundSlow[3]": "Amortiguador trasero lento izquierdo",
    "basicSetup.tyres.tyrePressure[0]": "Presión neumático delantero izquierdo",
    "basicSetup.tyres.tyrePressure[1]": "Presión neumático delantero derecho",
    "basicSetup.tyres.tyrePressure[2]": "Presión neumático trasero izquierdo",
    "basicSetup.tyres.tyrePressure[3]": "Presión neumático trasero derecho",
    "basicSetup.electronics.tC1": "Control de tracción TC1",
    "basicSetup.electronics.abs": "ABS",
    "advancedSetup.mechanicalBalance.brakeBias": "Balance de frenos"
}

# --- Cargar setup JSON ---
setup_file = st.file_uploader("📁 Cargar archivo de setup (.json)", type="json")

if setup_file:
    setup_data = json.load(setup_file)
    setup_original = copy.deepcopy(setup_data)
    st.success(f"Setup del coche cargado: {setup_data.get('carName', 'Desconocido')}")
else:
    st.info("Sube un archivo de setup para comenzar.")
    st.stop()

# --- Estado de modificaciones ---
if 'modificaciones' not in st.session_state:
    st.session_state.modificaciones = {}

# --- Menús en sidebar ---
categoria = st.sidebar.selectbox("Selecciona categoría", ["", "Aerodinámica", "Suspensión", "Neumáticos", "Electrónica", "Frenos"])

sintoma = ""
if categoria:
    sintomas_dict = {
        "Aerodinámica": ["", "Poca carga en curvas rápidas", "Demasiado drag en rectas", "Inestabilidad al frenar fuerte"],
        "Suspensión": ["", "El coche rebota al salir de curva", "Demasiado subviraje", "Demasiado sobreviraje"],
        "Neumáticos": ["", "Neumáticos delanteros demasiado calientes", "Neumáticos traseros fríos"],
        "Electrónica": ["", "Pierde tracción al salir de curvas", "Frenada inestable con ABS"],
        "Frenos": ["", "Bloquea fácilmente al frenar", "Frenada desigual en curva"]
    }
    sintoma = st.sidebar.selectbox("Selecciona síntoma", sintomas_dict[categoria])

# --- Recomendaciones automáticas ---
recomendaciones = {
    "Aerodinámica": {
        "Poca carga en curvas rápidas": {"advancedSetup.aeroBalance.rearWing": +1},
        "Demasiado drag en rectas": {"advancedSetup.aeroBalance.rearWing": -1},
        "Inestabilidad al frenar fuerte": {"advancedSetup.aeroBalance.rideHeight[1]": +1}
    },
    "Suspensión": {
        "El coche rebota al salir de curva": {"advancedSetup.dampers.reboundSlow[2]": -1, "advancedSetup.dampers.reboundSlow[3]": -1},
        "Demasiado subviraje": {"advancedSetup.mechanicalBalance.aRBFront": -1},
        "Demasiado sobreviraje": {"advancedSetup.mechanicalBalance.aRBRear": -1}
    },
    "Neumáticos": {
        "Neumáticos delanteros demasiado calientes": {"basicSetup.tyres.tyrePressure[0]": -1, "basicSetup.tyres.tyrePressure[1]": -1},
        "Neumáticos traseros fríos": {"basicSetup.tyres.tyrePressure[2]": +1, "basicSetup.tyres.tyrePressure[3]": +1}
    },
    "Electrónica": {
        "Pierde tracción al salir de curvas": {"basicSetup.electronics.tC1": +1},
        "Frenada inestable con ABS": {"basicSetup.electronics.abs": -1}
    },
    "Frenos": {
        "Bloquea fácilmente al frenar": {"advancedSetup.mechanicalBalance.brakeBias": -1},
        "Frenada desigual en curva": {"advancedSetup.mechanicalBalance.brakeBias": +1}
    }
}

# --- Mostrar recomendaciones y aplicar ---
if sintoma and sintoma != "":
    st.subheader(f"Recomendaciones para: {sintoma}")
    recs = recomendaciones[categoria][sintoma]
    for param, delta in recs.items():
        desc = param_desc.get(param, param)
        st.write(f"**{desc}**: aplicar cambio {delta}")
        if st.button(f"Aplicar {desc}", key=f"aplicar_{param}"):
            st.session_state.modificaciones[param] = delta
            st.success(f"✅ Recomendación '{desc}' añadida al setup")

# --- Panel de resumen acumulativo ---
st.subheader("🔍 Resumen acumulativo de cambios")
if st.session_state.modificaciones:
    tabla = []
    for param, delta in st.session_state.modificaciones.items():
        partes = param.replace(']', '').replace('[', '.').split('.')[1:]
        valor_original = get_valor_json(setup_original, partes)
        if isinstance(valor_original, (int, float)):
            valor_mod = valor_original + delta
            diferencia = valor_mod - valor_original
        else:
            valor_mod = valor_original
            diferencia = "-"
        tabla.append((param, valor_original, valor_mod, diferencia))

    st.table([{"Parámetro": param_desc.get(p, p), "Original": o, "Modificado": m, "Diferencia": d} for p, o, m, d in tabla])

    if st.button("💾 Exportar setup modificado"):
        setup_mod = copy.deepcopy(setup_original)
        for p, o, m, d in tabla:
            partes = p.replace(']', '').replace('[', '.').split('.')[1:]
            set_valor_json(setup_mod, partes, m)
        st.download_button("⬇️ Descargar setup modificado", data=json.dumps(setup_mod, indent=2), file_name="setup_modificado.json")
else:
    st.info("Aún no has aplicado ninguna recomendación.")

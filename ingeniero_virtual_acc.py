import streamlit as st
import json
import copy

st.set_page_config(page_title="Ingeniero Virtual ACC", layout="wide")
st.title("🏎️ Ingeniero Virtual ACC")

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
        st.write(f"**{param}**: aplicar cambio {delta}")
        if st.button(f"Aplicar {param}", key=f"aplicar_{param}"):
            st.session_state.modificaciones[param] = delta
            st.success(f"✅ Recomendación '{param}' añadida al setup")

# --- Panel de resumen acumulativo ---
st.subheader("🔍 Resumen acumulativo de cambios")
if st.session_state.modificaciones:
    tabla = []
    for param, delta in st.session_state.modificaciones.items():
        partes = param.replace(']', '').replace('[', '.').split('.')
        temp = setup_original
        for p in partes[1:]:
            temp = temp[int(p)] if p.isdigit() else temp.get(p)
        valor_original = temp
        valor_mod = valor_original + delta if isinstance(valor_original, (int, float)) else valor_original
        tabla.append((param, valor_original, valor_mod, valor_mod - valor_original))

    st.table([{"Parámetro": p, "Original": o, "Modificado": m, "Diferencia": d} for p, o, m, d in tabla])

    if st.button("💾 Exportar setup modificado"):
        setup_mod = copy.deepcopy(setup_original)
        for p, o, m, d in tabla:
            partes = p.replace(']', '').replace('[', '.').split('.')
            temp = setup_mod
            for sub in partes[1:-1]:
                temp = temp[int(sub)] if sub.isdigit() else temp[sub]
            ult = partes[-1]
            if ult.isdigit():
                temp[int(ult)] = m
            else:
                temp[ult] = m
        st.download_button("⬇️ Descargar setup modificado", data=json.dumps(setup_mod, indent=2), file_name="setup_modificado.json")
else:
    st.info("Aún no has aplicado ninguna recomendación.")
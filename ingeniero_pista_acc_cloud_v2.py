import streamlit as st
import json
import copy

st.set_page_config(page_title="Ingeniero de Pista Virtual - ACC", layout="wide")

st.title("🏎️ Ingeniero de Pista Virtual - Assetto Corsa Competizione")

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

# --- Menús de diagnóstico ---
menu = st.sidebar.selectbox("Selecciona una categoría:", [
    "Aerodinámica",
    "Suspensión",
    "Neumáticos",
    "Electrónica",
    "Frenos"
])

# Diccionario de síntomas y sugerencias reales en ACC
sintomas = {
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

sintoma = st.selectbox("Selecciona un síntoma:", list(sintomas[menu].keys()))

if st.button("💡 Agregar recomendación"):
    st.session_state.modificaciones.update(sintomas[menu][sintoma])
    st.success("Recomendación agregada al resumen acumulativo.")

# --- Panel de vista previa de cambios ---
st.subheader("🔍 Vista previa de modificaciones acumuladas")

if not st.session_state.modificaciones:
    st.info("Aún no has agregado recomendaciones.")
else:
    tabla = []
    for param, delta in st.session_state.modificaciones.items():
        # Obtener valor original
        partes = param.replace(']', '').replace('[', '.').split('.')
        temp = setup_original
        for p in partes[1:]:
            temp = temp[int(p)] if p.isdigit() else temp.get(p)
        valor_original = temp

        valor_mod = valor_original + delta if isinstance(valor_original, (int, float)) else valor_original
        aplicar = st.checkbox(f"Aplicar cambio en {param}", value=True, key=param)
        if aplicar:
            tabla.append((param, valor_original, valor_mod))

    if tabla:
        st.table([{ 'Parámetro': p, 'Original': o, 'Modificado': m } for p, o, m in tabla])

        if st.button("💾 Exportar setup modificado"):
            setup_mod = copy.deepcopy(setup_original)

            # Aplicar solo los seleccionados
            for p, o, m in tabla:
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
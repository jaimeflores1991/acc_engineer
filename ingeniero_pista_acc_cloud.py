import streamlit as st
import json
from copy import deepcopy

st.set_page_config(page_title="Ingeniero de Pista Virtual ACC", layout="wide")

st.title("Ingeniero de Pista Virtual ACC — Prototipo v2")
st.markdown("""
Carga un setup real de ACC (.json), selecciona síntomas y recibe recomendaciones de ajustes.
Puedes aplicar cambios por pasos fijos, ver valores modificados y exportar un nuevo setup.
""")

# ----- Funciones de utilidad -----

def load_json(file_buffer):
    try:
        data = json.load(file_buffer)
        return data
    except Exception as e:
        st.error(f"Error al cargar JSON: {e}")
        return None


def save_json(data, filename="setup_modificado.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def apply_change(setup, path, delta):
    """Aplica un cambio numérico a la ruta del JSON"""  
    keys = path.split('.')
    obj = setup
    for k in keys[:-1]:
        obj = obj[k]
    key_last = keys[-1]
    original = obj[key_last]
    obj[key_last] = round(original + delta, 3) if isinstance(original, (int, float)) else obj[key_last]
    return original, obj[key_last]

# ----- State -----
if "setup_original" not in st.session_state:
    st.session_state.setup_original = None
if "setup_modificado" not in st.session_state:
    st.session_state.setup_modificado = None
if "historial_cambios" not in st.session_state:
    st.session_state.historial_cambios = []

# ----- Panel lateral: Cargar Setup -----
st.sidebar.header("Carga de Setup")
setup_file = st.sidebar.file_uploader("Cargar archivo JSON de setup de ACC", type="json")

if setup_file:
    setup = load_json(setup_file)
    if setup:
        st.session_state.setup_original = deepcopy(setup)
        st.session_state.setup_modificado = deepcopy(setup)
        st.session_state.historial_cambios = []
        st.success(f"Setup '{setup.get('carName','Sin nombre')}' cargado correctamente!")

# ----- Menús de diagnóstico estilo PC2 -----
if st.session_state.setup_modificado:

    st.header("Menú de diagnóstico — Project Cars 2 style")

    categorias = {
        "Motor / Transmisión": {
            "No llego a velocidad máxima": [
                {"path": "advancedSetup.aeroBalance.rearWing", "delta": -1, "desc": "Reduce ángulo alerón trasero 1 punto"},
                {"path": "basicSetup.tyres.tyrePressure", "delta": 0.2, "desc": "Aumenta presión neumáticos delanteros 0.2 PSI"}
            ],
            "Las RPM son muy altas en recta": [
                {"path": "advancedSetup.drivetrain.preload", "delta": -1, "desc": "Reduce preload diferencial 1 unidad"}
            ]
        },
        "Suspensión": {
            "El coche rebota al salir de curva": [
                {"path": "advancedSetup.dampers.reboundFast", "delta": 1, "desc": "Endurece amortiguador rápido 1 punto"}
            ]
        },
        "Neumáticos": {
            "No alcanzo temperatura óptima": [
                {"path": "basicSetup.tyres.tyrePressure", "delta": -0.3, "desc": "Reduce presión neumáticos 0.3 PSI"}
            ]
        }
    }

    categoria_sel = st.selectbox("Selecciona categoría:", options=[""]+list(categorias.keys()))

    if categoria_sel:
        sintomas = categorias[categoria_sel]
        sintoma_sel = st.selectbox("Selecciona síntoma:", options=[""]+list(sintomas.keys()))

        if sintoma_sel:
            st.subheader("Recomendaciones de ajuste")
            cambios_sugeridos = sintomas[sintoma_sel]

            aplicar_cambios = []
            for c in cambios_sugeridos:
                checkbox = st.checkbox(f"{c['desc']}")
                aplicar_cambios.append((checkbox, c))

            if st.button("Aplicar cambios seleccionados"):
                for chk, c in aplicar_cambios:
                    if chk:
                        path = c['path']
                        delta = c['delta']
                        original, nuevo = apply_change(st.session_state.setup_modificado, path, delta)
                        st.session_state.historial_cambios.append({"path": path, "original": original, "nuevo": nuevo, "desc": c['desc']})
                st.success("Cambios aplicados!")

            if st.session_state.historial_cambios:
                st.subheader("Historial de cambios aplicados")
                for i, h in enumerate(st.session_state.historial_cambios[::-1], 1):
                    st.write(f"{i}. {h['desc']}: {h['original']} → {h['nuevo']}")

            if st.button("Exportar setup modificado"):
                filename = f"{st.session_state.setup_modificado.get('carName','setup')}_mod.json"
                save_json(st.session_state.setup_modificado, filename)
                st.success(f"Setup exportado como {filename}")

else:
    st.info("Carga un setup JSON para comenzar a ver recomendaciones y aplicar ajustes.")

st.caption("Prototipo v2 — Ingeniero de Pista Virtual ACC. Valores modificados visibles, pasos fijos, historial de cambios y exportación selectiva.")
import streamlit as st
import json
import copy

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="centered")

# ----------------------------------
# Estado inicial
# ----------------------------------
if "setup" not in st.session_state:
    st.session_state.setup = None
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "home"
if "menu_seleccionado" not in st.session_state:
    st.session_state.menu_seleccionado = None
if "recomendaciones" not in st.session_state:
    st.session_state.recomendaciones = []

# ----------------------------------
# Parámetros ACC amigables
# ----------------------------------
param_friendly = {
    # Frenos
    "frontal_presion_frenos": "Presión frenos delanteros",
    "frontal_reparto_frenada": "Reparto de frenada delantero",
    "trasero_presion_frenos": "Presión frenos traseros",
    "trasero_reparto_frenada": "Reparto de frenada trasero",
    # Aerodinámica
    "delantero_ala": "Alerón delantero",
    "trasero_ala": "Alerón trasero",
    "splitter": "Splitter delantero",
    # Agarre mecánico / suspensión
    "barra_estabilizadora_delantera": "Barra estabilizadora delantera",
    "barra_estabilizadora_trasera": "Barra estabilizadora trasera",
    "rigidez_delantera": "Rigidez delantera",
    "rigidez_trasera": "Rigidez trasera",
    "altura_marcha_delantera": "Altura de marcha delantera",
    "altura_marcha_trasera": "Altura de marcha trasera",
    # Electrónica
    "TC": "Control de tracción",
    "ABS": "ABS",
    "ECUMap": "ECUMap",
    "TC2": "TC2",
    # Amortiguadores
    "bump_slow_front": "Bump slow delantero",
    "bump_fast_front": "Bump fast delantero",
    "rebound_slow_front": "Rebound slow delantero",
    "rebound_fast_front": "Rebound fast delantero",
    # Neumáticos
    "tyre_psi_fl": "PSI delantero izquierdo",
    "tyre_psi_fr": "PSI delantero derecho",
    "tyre_psi_rl": "PSI trasero izquierdo",
    "tyre_psi_rr": "PSI trasero derecho",
    "camber_fl": "Caída delantero izquierdo",
    "camber_fr": "Caída delantero derecho",
    "camber_rl": "Caída trasero izquierdo",
    "camber_rr": "Caída trasero derecho",
    "toe_fl": "Toe delantero izquierdo",
    "toe_fr": "Toe delantero derecho",
    "toe_rl": "Toe trasero izquierdo",
    "toe_rr": "Toe trasero derecho",
}

# ----------------------------------
# Síntomas a parámetros ACC
# ----------------------------------
sintoma_param = {
    # Frenos
    "No se detiene a tiempo": ["frontal_presion_frenos", "frontal_reparto_frenada"],
    "Se detiene muy pronto": ["frontal_presion_frenos"],
    "Patina cuando freno delantero": ["frontal_presion_frenos", "frontal_reparto_frenada"],
    "Patina cuando freno trasero": ["trasero_presion_frenos", "trasero_reparto_frenada"],
    # Aerodinámica
    "Voy muy lento en rectas": ["delantero_ala", "trasero_ala"],
    "Patino en curvas rápidas": ["trasero_ala"],
    "El auto no gira en curvas": ["delantero_ala", "trasero_ala"],
    # Suspensión / Agarre Mecánico
    "El auto no gira al entrar a curva": ["rigidez_delantera", "altura_marcha_delantera"],
    "El auto gira demasiado al entrar a curva": ["barra_estabilizadora_delantera", "rigidez_delantera"],
    "Neumáticos se desgastan y no responden": ["rigidez_delantera", "rigidez_trasera"],
    # Electrónica
    "Acelera muy despacio": ["TC", "ECUMap"],
    "Velocidad máxima insuficiente": ["TC", "ABS"],
    # Amortiguadores
    "El auto rebota demasiado": ["bump_fast_front", "rebound_fast_front"],
    "El auto se hunde al frenar": ["bump_slow_front"],
    # Neumáticos
    "Presión baja/alta": ["tyre_psi_fl", "tyre_psi_fr", "tyre_psi_rl", "tyre_psi_rr"],
    "Desgaste desigual": ["camber_fl", "camber_fr", "camber_rl", "camber_rr",
                          "toe_fl", "toe_fr", "toe_rl", "toe_rr"]
}

# ----------------------------------
# Función para generar recomendación
# ----------------------------------
def generar_recomendacion(sintoma):
    params = sintoma_param.get(sintoma, [])
    recomendaciones = []
    for p in params:
        valor_actual = None
        # Buscar valor actual en setup
        if st.session_state.setup:
            for sec in ["basicSetup", "advancedSetup"]:
                if sec in st.session_state.setup:
                    if p in st.session_state.setup[sec].get("mechanicalBalance", {}):
                        valor_actual = st.session_state.setup[sec]["mechanicalBalance"][p]
                        break
        if valor_actual is not None:
            recomendaciones.append(f"Aumentar {param_friendly.get(p,p)} de {valor_actual} → {valor_actual + 1}")
        else:
            recomendaciones.append(f"Aumentar {param_friendly.get(p,p)} 1 punto")
    return " | ".join(recomendaciones)

# ----------------------------------
# Home
# ----------------------------------
if st.session_state.pagina_actual == "home":
    st.title("Ingeniero de Pista ACC")
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    
    archivo_setup = st.file_uploader("Cargar archivo de setup", type=["json"])
    if archivo_setup:
        try:
            st.session_state.setup = json.load(archivo_setup)
            st.session_state.pagina_actual = "menu_principal"
        except:
            st.error("Archivo inválido")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continuar sin cargar setup", key="continuar_setup"):
        st.session_state.pagina_actual = "menu_principal"
    
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------
# Menú principal
# ----------------------------------
elif st.session_state.pagina_actual == "menu_principal":
    st.title("Menú principal")
    categorias = ["Frenos", "Aerodinámica", "Suspensión", "Electrónica", "Amortiguadores", "Neumáticos"]
    cols = st.columns(len(categorias))
    for i, c in enumerate(categorias):
        with cols[i]:
            if st.button(c, key=f"menu_{c}"):
                st.session_state.menu_seleccionado = c
                st.session_state.pagina_actual = "submenu"

# ----------------------------------
# Submenú de categoría
# ----------------------------------
elif st.session_state.pagina_actual == "submenu":
    categoria = st.session_state.menu_seleccionado
    st.title(f"{categoria}")
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)

    sintomas_por_categoria = {
        "Frenos": ["No se detiene a tiempo", "Se detiene muy pronto",
                   "Patina cuando freno delantero", "Patina cuando freno trasero"],
        "Aerodinámica": ["Voy muy lento en rectas", "Patino en curvas rápidas", "El auto no gira en curvas"],
        "Suspensión": ["El auto no gira al entrar a curva", "El auto gira demasiado al entrar a curva",
                       "Neumáticos se desgastan y no responden"],
        "Electrónica": ["Acelera muy despacio", "Velocidad máxima insuficiente"],
        "Amortiguadores": ["El auto rebota demasiado", "El auto se hunde al frenar"],
        "Neumáticos": ["Presión baja/alta", "Desgaste desigual"]
    }

    for s in sintomas_por_categoria.get(categoria, []):
        if st.button(s, key=f"{categoria}_{s}"):
            rec = generar_recomendacion(s)
            st.session_state.recomendaciones.append(rec)

    st.markdown("<br>", unsafe_allow_html=True)
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
# Exportar setup
# ----------------------------------
if st.session_state.pagina_actual == "submenu" and st.session_state.setup:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Exportar setup modificado"):
        # Aplicar recomendaciones
        setup_mod = copy.deepcopy(st.session_state.setup)
        for rec in st.session_state.recomendaciones:
            for key, friendly in param_friendly.items():
                if friendly in rec:
                    # Aumentar valor +1 (simplificado)
                    try:
                        for sec in ["basicSetup", "advancedSetup"]:
                            if sec in setup_mod and key in setup_mod[sec].get("mechanicalBalance", {}):
                                setup_mod[sec]["mechanicalBalance"][key] += 1
                    except:
                        pass
        # Descargar archivo
        st.download_button("Descargar setup modificado", data=json.dumps(setup_mod, indent=2), file_name="setup_mod.json")

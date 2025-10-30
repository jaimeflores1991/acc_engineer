# ingeniero_virtual_acc.py
import streamlit as st
import json
import copy
from recomendaciones import RECOMENDACIONES

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="centered")

# ---------------------------
# Helpers
# ---------------------------
def fmt_accion(a):
    val = a.get("change", "")
    unit = a.get("unit", "")
    if unit in ["punto", "pts"]:
        unit_text = " pts"
    elif unit == "deg":
        unit_text = "°"
    elif unit == "psi":
        unit_text = " psi"
    elif unit == "mm":
        unit_text = " mm"
    elif unit == "Nm":
        unit_text = " Nm"
    elif unit == "%":
        unit_text = " %"
    else:
        unit_text = f" {unit}" if unit else ""
    return f"{a.get('accion')} {val}{unit_text}"

def apply_change_to_setup(setup, change):
    path = change.get("path")
    if not path or not isinstance(path, list):
        return False, "Ruta inválida en la recomendación."

    temp = setup
    try:
        for key in path[:-1]:
            if isinstance(key, int):
                if not isinstance(temp, list) or key >= len(temp):
                    return False, f"Índice {key} fuera de rango en ruta {path}"
                temp = temp[key]
            else:
                if key not in temp:
                    return False, f"Clave '{key}' no existe en setup"
                temp = temp[key]

        final = path[-1]
        if isinstance(final, int):
            if not isinstance(temp, list) or final >= len(temp):
                return False, f"Índice final {final} fuera de rango en ruta {path}"
            current = temp[final]
        else:
            if final not in temp:
                return False, f"Clave final '{final}' no existe en setup"
            current = temp[final]

        ch = str(change.get("change"))
        if ch.startswith("+") or ch.startswith("-"):
            delta = float(ch)
            new_val = float(current) + delta
        else:
            new_val = float(ch)

        if isinstance(final, int):
            temp[final] = new_val
        else:
            temp[final] = new_val

        return True, None
    except Exception as e:
        return False, f"Error aplicando cambio: {e}"


# ---------------------------
# Session state init
# ---------------------------
if "setup_loaded" not in st.session_state:
    st.session_state.setup_loaded = False
if "setup_data" not in st.session_state:
    st.session_state.setup_data = None
if "menu" not in st.session_state:
    st.session_state.menu = "home"
if "categoria" not in st.session_state:
    st.session_state.categoria = None
if "sintoma_activo" not in st.session_state:
    st.session_state.sintoma_activo = None
if "acciones_selected" not in st.session_state:
    st.session_state.acciones_selected = []
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# ---------------------------
# HOME
# ---------------------------
if st.session_state.menu == "home":
    st.title("🧠 Ingeniero de Pista — ACC")
    st.write("Carga tu setup o continúa sin cargar uno para explorar recomendaciones.")
    uploaded = st.file_uploader("📂 Cargar setup ACC (.json)", type=["json"])

    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if uploaded and st.button("Cargar setup", use_container_width=False):
        try:
            st.session_state.setup_data = json.load(uploaded)
            st.session_state.setup_loaded = True
            st.session_state.menu = "menu"
        except Exception as e:
            st.error(f"Error leyendo JSON: {e}")

    if st.button("➡ Continuar sin cargar setup", use_container_width=False):
        st.session_state.setup_loaded = False
        st.session_state.menu = "menu"
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------
# MENÚ PRINCIPAL
# ---------------------------
elif st.session_state.menu == "menu":
    st.header("Selecciona una categoría:")
    categorias = list(RECOMENDACIONES.keys())

    st.markdown("<div style='display:flex;flex-direction:column;align-items:center;'>", unsafe_allow_html=True)
    for c in categorias:
        if st.button(c, key=f"cat_{c}", use_container_width=True):
            st.session_state.categoria = c
            st.session_state.menu = "submenu"
            st.session_state.sintoma_activo = None
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("📋 Ver resumen / exportar", use_container_width=True):
        st.session_state.menu = "resumen"


# ---------------------------
# SUBMENÚ (síntomas y acciones)
# ---------------------------
elif st.session_state.menu == "submenu":
    cat = st.session_state.categoria
    st.header(cat)
    sintomas = RECOMENDACIONES.get(cat, {})

    # Mostrar síntomas
    st.markdown("<div style='display:flex;flex-direction:column;align-items:center;'>", unsafe_allow_html=True)
    for sintoma in sintomas.keys():
        if st.button(sintoma, key=f"s_{sintoma}", use_container_width=True):
            st.session_state.sintoma_activo = sintoma
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Mostrar acciones
    if st.session_state.sintoma_activo:
        s = st.session_state.sintoma_activo
        st.subheader(f"Acciones para: {s}")
        acciones = RECOMENDACIONES[cat][s]

        for idx, accion in enumerate(acciones):
            texto = fmt_accion(accion)
            st.markdown(
                f"<div style='text-align:center;margin-bottom:10px;'>"
                f"<button style='background-color:#444;border:none;color:white;padding:10px 20px;border-radius:12px;width:90%;cursor:pointer;' "
                f"onclick='window.parent.postMessage({{type:\"streamlit:buttonClicked\", key:\"add_{cat}_{s}_{idx}\"}}, \"*\")'>"
                f"{texto}</button></div>",
                unsafe_allow_html=True,
            )

            add_key = f"add_{cat}_{s}_{idx}"
            if st.button(f"Agregar: {texto}", key=add_key, use_container_width=True):
                st.session_state.acciones_selected.append({
                    "categoria": cat,
                    "sintoma": s,
                    "accion": accion
                })
                st.success(f"Agregado: {texto}")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Volver al menú principal", use_container_width=True):
            st.session_state.menu = "menu"
    with col2:
        if st.button("📋 Ver resumen", use_container_width=True):
            st.session_state.menu = "resumen"


# ---------------------------
# RESUMEN
# ---------------------------
elif st.session_state.menu == "resumen":
    st.header("Resumen de acciones seleccionadas")

    if not st.session_state.acciones_selected:
        st.info("No hay acciones agregadas.")
    else:
        to_remove = None
        for i, item in enumerate(st.session_state.acciones_selected):
            cat = item["categoria"]
            s = item["sintoma"]
            accion = item["accion"]
            texto = fmt_accion(accion)
            cols = st.columns([0.8, 0.2])
            with cols[0]:
                st.write(f"**{cat} — {s}:** {texto}")
            with cols[1]:
                if st.button("❌", key=f"del_{i}"):
                    to_remove = i
        if to_remove is not None:
            st.session_state.acciones_selected.pop(to_remove)
            st.experimental_rerun()

        st.markdown("---")
        if st.button("💾 Exportar setup con cambios"):
            if not st.session_state.setup_loaded:
                st.warning("Debes cargar un setup primero.")
            else:
                setup_mod = copy.deepcopy(st.session_state.setup_data)
                for item in st.session_state.acciones_selected:
                    accion = item["accion"]
                    if isinstance(accion, list):
                        for sub in accion:
                            apply_change_to_setup(setup_mod, sub)
                    else:
                        apply_change_to_setup(setup_mod, accion)
                st.download_button(
                    "⬇ Descargar setup modificado",
                    data=json.dumps(setup_mod, indent=2),
                    file_name="setup_modificado.json",
                    mime="application/json"
                )

    st.markdown("---")
    if st.button("⬅ Volver al menú principal"):
        st.session_state.menu = "menu"

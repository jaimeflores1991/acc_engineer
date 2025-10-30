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
    """Formato legible para una acción dict de RECOMENDACIONES."""
    val = a.get("change", "")
    unit = a.get("unit", "")
    if unit == "punto" or unit == "pts":
        unit_text = " pts"
    elif unit == "deg":
        unit_text = "°"
    elif unit == "psi":
        unit_text = " psi"
    elif unit == "mm":
        unit_text = " mm"
    elif unit == "Nm":
        unit_text = " Nm"
    else:
        unit_text = f" {unit}" if unit else ""
    return f"{a.get('accion')} {val}{unit_text}"

def apply_change_to_setup(setup, change):
    """
    Aplica un cambio (dict con 'path' y 'change') al setup (dict).
    'change' suele estar en formato "+1", "-0.1" o "1.0" (absoluto).
    'path' es una lista como ["basicSetup","tyres","tyrePressure",0]
    Devuelve (True, None) si aplicado, o (False, mensaje) si falla.
    """
    path = change.get("path")
    if not path or not isinstance(path, list):
        return False, "Ruta inválida en la recomendación."

    # Navegar hasta el contenedor que tiene la clave/índice final
    temp = setup
    try:
        for key in path[:-1]:
            # si key es entero (índice)
            if isinstance(key, int):
                # temp debe ser lista
                if not isinstance(temp, list) or key >= len(temp):
                    return False, f"Índice {key} fuera de rango en ruta {path}"
                temp = temp[key]
            else:
                # string key
                if key not in temp:
                    return False, f"Clave '{key}' no existe en setup"
                temp = temp[key]
        final = path[-1]
        # obtener el valor actual
        if isinstance(final, int):
            if not isinstance(temp, list) or final >= len(temp):
                return False, f"Índice final {final} fuera de rango en ruta {path}"
            current = temp[final]
        else:
            if final not in temp:
                return False, f"Clave final '{final}' no existe en setup"
            current = temp[final]

        # parse change
        ch = str(change.get("change"))
        if ch.startswith("+") or ch.startswith("-"):
            delta = float(ch)
            # aplicar suma
            new_val = float(current) + delta
        else:
            new_val = float(ch)

        # escribir de vuelta
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
    st.session_state.setup_loaded = False      # True únicamente si subes archivo
if "setup_data" not in st.session_state:
    st.session_state.setup_data = None        # dict con JSON si cargado
if "menu" not in st.session_state:
    st.session_state.menu = "home"            # home, menu, submenu, resumen
if "categoria" not in st.session_state:
    st.session_state.categoria = None
if "sintoma_activo" not in st.session_state:
    st.session_state.sintoma_activo = None
if "acciones_selected" not in st.session_state:
    st.session_state.acciones_selected = []   # lista de dicts {categoria,sintoma,accion_index}
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []            # mensajes de log para usuario


# ---------------------------
# UI: Home
# ---------------------------
st.title("🧠 Ingeniero de Pista — ACC (versión final)")
st.write("Carga tu setup (JSON) para aplicar cambios directos, o continúa sin setup para explorar recomendaciones.")

if st.session_state.menu == "home":
    uploaded = st.file_uploader("📂 Cargar setup ACC (.json)", type=["json"])
    col1, col2 = st.columns([1,1])
    with col1:
        if uploaded:
            if st.button("Cargar setup"):
                try:
                    st.session_state.setup_data = json.load(uploaded)
                    st.session_state.setup_loaded = True
                    st.session_state.menu = "menu"
                    st.session_state.mensajes.append("Setup cargado correctamente.")
                except Exception as e:
                    st.error(f"Error leyendo JSON: {e}")
    with col2:
        if st.button("Continuar sin cargar setup"):
            st.session_state.setup_data = None
            st.session_state.setup_loaded = False
            st.session_state.menu = "menu"

    st.markdown("---")
    if st.session_state.mensajes:
        for m in st.session_state.mensajes[-3:]:
            st.info(m)


# ---------------------------
# UI: Menú principal
# ---------------------------
if st.session_state.menu == "menu":
    st.header("Menú principal")
    st.write("Selecciona una categoría:")
    categorias = list(RECOMENDACIONES.keys())
    for c in categorias:
        if st.button(c, key=f"cat_{c}", use_container_width=True):
            st.session_state.categoria = c
            st.session_state.sintoma_activo = None
            st.session_state.menu = "submenu"

    st.markdown("---")
    if st.button("📋 Ver resumen / exportar", use_container_width=True):
        st.session_state.menu = "resumen"

# ---------------------------
# UI: Submenu (síntomas y acciones)
# ---------------------------
if st.session_state.menu == "submenu":
    cat = st.session_state.categoria
    st.header(f"{cat}")
    st.write("Selecciona un síntoma para ver las acciones recomendadas:")
    sintomas = RECOMENDACIONES.get(cat, {})

    # mostrar botones de sintomas
    for sintoma in sintomas.keys():
        if st.button(sintoma, key=f"s_{sintoma}", use_container_width=True):
            st.session_state.sintoma_activo = sintoma

    st.markdown("---")
    # si hay sintoma activo mostrar acciones
    if st.session_state.sintoma_activo:
        s = st.session_state.sintoma_activo
        st.subheader(f"Acciones sugeridas para: {s}")
        acciones = RECOMENDACIONES[cat][s]
        for idx, accion in enumerate(acciones):
            texto = fmt_accion(accion)
            cols = st.columns([0.8, 0.2])
            with cols[0]:
                st.write(f"**{texto}**")
                if accion.get("desc"):
                    st.caption(accion["desc"])
            with cols[1]:
                add_key = f"add_{cat}_{s}_{idx}"
                if st.button("✅", key=add_key):
                    # Añadir acción específica al arreglo de seleccionadas
                    st.session_state.acciones_selected.append({
                        "categoria": cat,
                        "sintoma": s,
                        "accion": accion
                    })
                    st.success(f"Agregado: {texto}")

    st.markdown("---")
    col1, col2 = st.columns([0.5,0.5])
    with col1:
        if st.button("⬅ Volver al menú principal", use_container_width=True):
            st.session_state.menu = "menu"
            st.session_state.categoria = None
            st.session_state.sintoma_activo = None
    with col2:
        if st.button("📋 Ir a resumen"):
            st.session_state.menu = "resumen"

# ---------------------------
# UI: Resumen y Exportación
# ---------------------------
if st.session_state.menu == "resumen":
    st.header("Resumen de acciones seleccionadas")
    if not st.session_state.acciones_selected:
        st.info("Aún no has agregado acciones. Ve a una categoría y selecciona un síntoma.")
    else:
        # Mostrar con posibilidad de excluir / borrar
        to_remove = None
        include_mask = []
        st.write("Marca las acciones que quieres aplicar al exportar (por defecto todas seleccionadas):")
        for i, item in enumerate(st.session_state.acciones_selected):
            cat = item["categoria"]
            s = item["sintoma"]
            accion = item["accion"]
            texto = fmt_accion(accion)
            cols = st.columns([0.8, 0.1, 0.1])
            with cols[0]:
                checked = st.checkbox(f"{cat} — {s} → {texto}", value=True, key=f"sel_{i}")
                include_mask.append(bool(checked))
            with cols[1]:
                if st.button("❌", key=f"del_{i}"):
                    to_remove = i
            with cols[2]:
                st.caption(accion.get("unit",""))

        if to_remove is not None:
            st.session_state.acciones_selected.pop(to_remove)
            st.experimental_rerun()

        st.markdown("---")
        # Si no hay setup cargado, no aplicar pero permitir descargar resumen y pedir cargar
        if not st.session_state.setup_loaded:
            st.warning("No has cargado un setup. Si quieres aplicar los cambios al JSON debes cargar uno ahora.")
            uploaded_for_export = st.file_uploader("Carga el setup al que aplicar los cambios (para exportar)", type=["json"])
            if uploaded_for_export:
                if st.button("Cargar y aplicar cambios"):
                    try:
                        st.session_state.setup_data = json.load(uploaded_for_export)
                        st.session_state.setup_loaded = True
                        st.success("Setup cargado. Ahora aplicaremos los cambios seleccionados.")
                    except Exception as e:
                        st.error(f"Error leyendo JSON: {e}")

        # Botón aplicar y exportar (solo si setup cargado)
        selected_indices = [i for i, v in enumerate(include_mask) if v]
        if st.button("💾 Aplicar cambios y exportar setup (JSON)"):
            if not st.session_state.setup_loaded or st.session_state.setup_data is None:
                st.error("Debes cargar un setup válido antes de exportar.")
            else:
                setup_mod = copy.deepcopy(st.session_state.setup_data)
                log = []
                for idx in selected_indices:
                    item = st.session_state.acciones_selected[idx]
                    accion = item["accion"]
                    # cada accion puede ser una lista (varias subacciones) o un dict con path/change
                    if isinstance(accion, list):
                        # lista de subacciones
                        for sub in accion:
                            ok, msg = apply_change_to_setup(setup_mod, sub)
                            log.append((sub, ok, msg))
                    else:
                        ok, msg = apply_change_to_setup(setup_mod, accion)
                        log.append((accion, ok, msg))

                # informar resultados
                success_count = sum(1 for _, ok, _ in log if ok)
                fail_entries = [m for _, ok, m in log if not ok]
                st.success(f"Intentadas {len(log)} modificaciones — exitosas: {success_count}")
                if fail_entries:
                    st.error("Algunas modificaciones no se pudieron aplicar:")
                    for f in fail_entries:
                        st.write(f"- {f}")

                # preparar descarga
                st.download_button(
                    "⬇ Descargar setup modificado (JSON)",
                    data=json.dumps(setup_mod, indent=2),
                    file_name="setup_modificado.json",
                    mime="application/json"
                )

        # También ofrecer descargar solo el resumen de acciones (sin aplicar)
        if st.button("⬇ Descargar resumen de acciones (JSON)"):
            resumen = {
                "acciones": st.session_state.acciones_selected
            }
            st.download_button(
                label="Descargar resumen (JSON)",
                data=json.dumps(resumen, indent=2),
                file_name="resumen_acciones.json",
                mime="application/json"
            )

    st.markdown("---")
    if st.button("⬅ Volver al menú principal"):
        st.session_state.menu = "menu"
        st.experimental_rerun()

# ---------------------------
# footer mensajes
# ---------------------------
if st.session_state.mensajes:
    for m in st.session_state.mensajes[-3:]:
        st.caption(m)

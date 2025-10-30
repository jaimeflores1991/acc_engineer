# ingeniero_virtual_acc.py
import streamlit as st
import json
from recomendaciones import RECOMENDACIONES

# Inicializar session_state
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "home"
if "setup" not in st.session_state:
    st.session_state.setup = None
if "selecciones" not in st.session_state:
    st.session_state.selecciones = []
if "categoria_actual" not in st.session_state:
    st.session_state.categoria_actual = None

# Función para aplicar recomendación
def aplicar_recomendacion(categoria, sintoma, recomendacion):
    st.session_state.selecciones.append({
        "categoria": categoria,
        "sintoma": sintoma,
        "accion": recomendacion["accion"],
        "change": recomendacion["change"],
        "unit": recomendacion["unit"],
        "desc": recomendacion.get("desc", "")
    })

# Función para mostrar botones de síntomas y recomendaciones
def mostrar_sintomas_y_recomendaciones(categoria):
    sintomas = RECOMENDACIONES.get(categoria, {})
    for sintoma, acciones in sintomas.items():
        st.markdown(f"### {sintoma}")
        for rec in acciones:
            if st.button(rec["accion"], key=f'{categoria}_{sintoma}_{rec["accion"]}'):
                aplicar_recomendacion(categoria, sintoma, rec)
        for rec in acciones:
            if rec.get("desc"):
                st.markdown(f"*{rec['desc']}*")
        st.markdown("---")

# ---- Pantallas ----
if st.session_state.pantalla == "home":
    st.write("")
    st.write("")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

    # Subida de setup
    uploaded_file = st.file_uploader("Cargar setup ACC (.json)", type=["json"])
    if uploaded_file is not None:
        try:
            st.session_state.setup = json.load(uploaded_file)
            st.session_state.pantalla = "menu_principal"
        except Exception as e:
            st.error(f"Error leyendo el setup: {e}")

    # Botón continuar sin setup
    if st.button("Continuar sin cargar setup", key="continuar", help="Puedes continuar sin setup, se usarán valores por defecto"):
        st.session_state.setup = None
        st.session_state.pantalla = "menu_principal"

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.pantalla == "menu_principal":
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("## Selecciona categoría")
    for cat in RECOMENDACIONES.keys():
        if st.button(cat, key=f"cat_{cat}"):
            st.session_state.categoria_actual = cat
            st.session_state.pantalla = "submenu"
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.pantalla == "submenu":
    categoria = st.session_state.categoria_actual
    st.markdown(f"## {categoria}")
    mostrar_sintomas_y_recomendaciones(categoria)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Volver al menú principal"):
        st.session_state.pantalla = "menu_principal"
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Resumen de recomendaciones ----
st.markdown("---")
st.markdown("## Resumen de recomendaciones seleccionadas")
if st.session_state.selecciones:
    for idx, sel in enumerate(st.session_state.selecciones):
        st.markdown(f"**{sel['categoria']} - {sel['sintoma']}**")
        st.markdown(f"- Acción: {sel['accion']} ({sel['change']} {sel['unit']})")
        if sel.get("desc"):
            st.markdown(f"  *{sel['desc']}*")
        if st.button("X", key=f"eliminar_{idx}"):
            st.session_state.selecciones.pop(idx)
else:
    st.markdown("No hay recomendaciones aplicadas aún.")

# ---- Exportar setup con recomendaciones ----
st.markdown("---")
if st.session_state.selecciones:
    if st.button("Exportar setup con recomendaciones"):
        export_data = {
            "setup": st.session_state.setup,
            "recomendaciones": st.session_state.selecciones
        }
        with open("setup_recomendado.json", "w") as f:
            json.dump(export_data, f, indent=2)
        st.success("Setup exportado como setup_recomendado.json")

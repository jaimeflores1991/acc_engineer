# ingeniero_virtual_acc.py
import streamlit as st
import json
from recomendaciones import RECOMENDACIONES

# ---- Inicializar session_state ----
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "home"
if "setup" not in st.session_state:
    st.session_state.setup = None
if "selecciones" not in st.session_state:
    st.session_state.selecciones = []
if "categoria_actual" not in st.session_state:
    st.session_state.categoria_actual = None

# ---- Funciones ----
def aplicar_recomendacion(categoria, sintoma, recomendacion):
    st.session_state.selecciones.append({
        "categoria": categoria,
        "sintoma": sintoma,
        "accion": recomendacion["accion"],
        "change": recomendacion["change"],
        "unit": recomendacion["unit"],
        "desc": recomendacion.get("desc", "")
    })
    st.toast(f"Aplicada: {recomendacion['accion']} ({recomendacion['change']} {recomendacion['unit']})")

def eliminar_recomendacion(idx):
    del st.session_state.selecciones[idx]

def mostrar_sintomas_y_recomendaciones(categoria):
    sintomas = RECOMENDACIONES.get(categoria, {})
    for sintoma, acciones in sintomas.items():
        st.markdown(f"### {sintoma}")
        for rec in acciones:
            if st.button(rec["accion"], key=f'{categoria}_{sintoma}_{rec["accion"]}'):
                aplicar_recomendacion(categoria, sintoma, rec)
            if rec.get("desc"):
                st.markdown(f"*{rec['desc']}*")
        st.markdown("---")

def reset_app():
    st.session_state.pantalla = "home"
    st.session_state.setup = None
    st.session_state.selecciones = []
    st.session_state.categoria_actual = None

# ---- Pantallas ----
if st.session_state.pantalla == "home":
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    archivo = st.file_uploader("Cargar setup ACC (.json)", type=["json"])
    col1, col2 = st.columns([1,1])
    with col1:
        if archivo is not None and st.button("Cargar setup"):
            try:
                st.session_state.setup = json.load(archivo)
                st.session_state.pantalla = "menu_principal"
            except Exception as e:
                st.error(f"Error leyendo el setup: {e}")
    with col2:
        if st.button("Continuar sin cargar setup"):
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
    if st.button("Volver al menú principal"):
        st.session_state.pantalla = "menu_principal"

# ---- Resumen de recomendaciones ----
if st.session_state.selecciones:
    st.markdown("---")
    st.markdown("## Resumen de recomendaciones aplicadas:")
    for idx, sel in enumerate(st.session_state.selecciones):
        cols = st.columns([8,1])
        with cols[0]:
            st.markdown(f"**{sel['categoria']} - {sel['sintoma']}**<br>- {sel['accion']} ({sel['change']} {sel['unit']})<br>{sel.get('desc','')}", unsafe_allow_html=True)
        with cols[1]:
            if st.button("X", key=f"del_{idx}"):
                eliminar_recomendacion(idx)
                st.experimental_rerun()

    if st.button("Limpiar todo y volver al inicio"):
        reset_app()

# ---- Exportar setup con recomendaciones ----
if st.session_state.selecciones:
    st.markdown("---")
    if st.button("Exportar setup con recomendaciones"):
        export_data = {
            "setup": st.session_state.setup,
            "recomendaciones": st.session_state.selecciones
        }
        with open("setup_recomendado.json", "w") as f:
            json.dump(export_data, f, indent=2)
        st.success("Setup exportado como setup_recomendado.json")

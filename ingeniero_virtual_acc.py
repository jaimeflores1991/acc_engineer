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
if "archivo_subido" not in st.session_state:
    st.session_state.archivo_subido = None

# ---- Funciones ----
def aplicar_recomendacion(categoria, sintoma, recomendacion):
    """Agrega recomendación al resumen y muestra notificación temporal"""
    st.session_state.selecciones.append({
        "categoria": categoria,
        "sintoma": sintoma,
        "accion": recomendacion["accion"],
        "change": recomendacion["change"],
        "unit": recomendacion["unit"],
        "desc": recomendacion.get("desc", "")
    })
    st.toast(f"Aplicada: {recomendacion['accion']} ({recomendacion['change']} {recomendacion['unit']})")

def mostrar_sintomas_y_recomendaciones(categoria):
    """Muestra los síntomas y botones de recomendaciones de forma limpia"""
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
    """Reinicia todo y vuelve al home"""
    st.session_state.pantalla = "home"
    st.session_state.setup = None
    st.session_state.selecciones = []
    st.session_state.categoria_actual = None
    st.session_state.archivo_subido = None

# ---- Pantallas ----
if st.session_state.pantalla == "home":
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    archivo = st.file_uploader("Cargar setup ACC (.json)", type=["json"], key="upld")
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
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Volver al menú principal"):
        st.session_state.pantalla = "menu_principal"
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Resumen de recomendaciones ----
if st.session_state.selecciones:
    st.markdown("---")
    st.markdown(
        """
        <div style='background-color: #e6e6e6; padding: 15px; border-radius: 8px; font-size: 0.9em;'>
        <strong>Resumen de recomendaciones aplicadas:</strong>
        """, unsafe_allow_html=True)
    for idx, sel in enumerate(st.session_state.selecciones):
        st.markdown(f"**{sel['categoria']} - {sel['sintoma']}**")
        st.markdown(f"- Acción: {sel['accion']} ({sel['change']} {sel['unit']})")
        if sel.get("desc"):
            st.markdown(f"  *{sel['desc']}*")
        if st.button("X", key=f"eliminar_{idx}"):
            st.session_state.selecciones.pop(idx)
    st.markdown("</div>", unsafe_allow_html=True)

    # Botón limpiar todo
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

import streamlit as st
import json
from io import BytesIO
from recomendaciones import RECOMENDACIONES as mapa_recomendaciones

st.set_page_config(page_title="Ingeniero de Pista ACC", layout="centered")

# ---------------- SESIÓN ----------------
if "menu_actual" not in st.session_state:
    st.session_state.menu_actual = "home"
if "setup" not in st.session_state:
    st.session_state.setup = None
if "recomendaciones_aplicadas" not in st.session_state:
    st.session_state.recomendaciones_aplicadas = []
if "cat_actual" not in st.session_state:
    st.session_state.cat_actual = None
if "sintoma_actual" not in st.session_state:
    st.session_state.sintoma_actual = None
if "setup_cargado" not in st.session_state:
    st.session_state.setup_cargado = False

# ---------------- FUNCIONES ----------------
def cargar_setup(file):
    try:
        st.session_state.setup = json.load(file)
        st.session_state.setup_cargado = True
        st.session_state.menu_actual = "menu_principal"
        st.success("Setup cargado correctamente. Ya puedes continuar.")
    except Exception as e:
        st.error(f"Error leyendo el setup: {e}")

def aplicar_recomendacion(cat, sintoma, rec_index):
    rec = mapa_recomendaciones[cat][sintoma][rec_index]
    st.session_state.recomendaciones_aplicadas.append({
        "categoria": cat,
        "sintoma": sintoma,
        "accion": rec["accion"],
        "change": rec["change"],
        "unit": rec["unit"],
        "desc": rec.get("desc","")
    })
    st.success(f"Aplicada: {rec['accion']}")

def borrar_recomendaciones():
    st.session_state.recomendaciones_aplicadas = []
    st.session_state.menu_actual = "home"
    st.session_state.setup = None
    st.session_state.cat_actual = None
    st.session_state.sintoma_actual = None
    st.session_state.setup_cargado = False

def exportar_setup():
    if st.session_state.setup:
        setup_bytes = BytesIO(json.dumps(st.session_state.setup, indent=2).encode())
        st.download_button("Descargar Setup Modificado", setup_bytes, "setup_modificado.json", "application/json")
    else:
        st.warning("No hay setup para exportar.")

# ---------------- HOME ----------------
if st.session_state.menu_actual == "home":
    st.title("Ingeniero de Pista ACC")
    st.write("Carga un setup o continúa sin setup.")

    file = st.file_uploader("Cargar setup (JSON ACC)", type="json")
    if file:
        cargar_setup(file)

    if st.button("Continuar sin setup"):
        st.session_state.menu_actual = "menu_principal"

# ---------------- MENÚ PRINCIPAL ----------------
if st.session_state.menu_actual == "menu_principal":
    st.title("Menú Principal")
    categorias = list(mapa_recomendaciones.keys())
    for cat in categorias:
        if st.button(cat):
            st.session_state.menu_actual = f"cat_{cat}"
            st.session_state.cat_actual = cat
            st.session_state.sintoma_actual = None

    # Resumen de recomendaciones aplicadas
    if st.session_state.recomendaciones_aplicadas:
        st.markdown("### Resumen de recomendaciones aplicadas:")
        for i, r in enumerate(st.session_state.recomendaciones_aplicadas):
            col1, col2 = st.columns([0.9,0.1])
            with col1:
                st.write(f"- **{r['accion']}** ({r['change']} {r['unit']})")
            with col2:
                if st.button("❌", key=f"borrar_{i}"):
                    st.session_state.recomendaciones_aplicadas.pop(i)
                    st.experimental_rerun = lambda: None
                    st.experimental_rerun()

    st.button("Borrar todo y volver al inicio", on_click=borrar_recomendaciones)
    exportar_setup()

# ---------------- CATEGORÍA ----------------
if st.session_state.menu_actual.startswith("cat_"):
    cat = st.session_state.cat_actual
    st.title(cat)

    sintomas = list(mapa_recomendaciones[cat].keys())
    for sintoma in sintomas:
        if st.session_state.sintoma_actual != sintoma:
            if st.button(sintoma):
                st.session_state.sintoma_actual = sintoma

    # Mostrar recomendaciones del síntoma seleccionado
    if st.session_state.sintoma_actual:
        sintoma = st.session_state.sintoma_actual
        st.subheader(f"Sintoma: {sintoma}")
        for i, rec in enumerate(mapa_recomendaciones[cat][sintoma]):
            if st.button(f"{rec['accion']} ({rec['change']} {rec['unit']})", key=f"{cat}_{sintoma}_{i}"):
                aplicar_recomendacion(cat, sintoma, i)
            st.caption(rec.get("desc",""))

        st.button("Volver al menú principal", on_click=lambda: setattr(st.session_state, 'menu_actual', 'menu_principal'))

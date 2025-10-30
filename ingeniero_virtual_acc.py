import streamlit as st
import json
from recomendaciones import RECOMENDACIONES

# =========================
# Funciones auxiliares
# =========================

def cargar_setup(file):
    try:
        return json.load(file)
    except Exception as e:
        st.error(f"Error cargando setup: {e}")
        return None

def exportar_setup(setup, filename="setup_modificado.json"):
    with open(filename, "w") as f:
        json.dump(setup, f, indent=4)
    st.success(f"Setup exportado como {filename}")

def aplicar_accion(setup, accion):
    # Aplica los cambios sobre el JSON del setup si está cargado
    if not setup:
        return
    path = accion.get("path", "")
    valor = accion.get("valor")
    if not path:
        return
    partes = path.split(".")
    temp = setup
    for p in partes[:-1]:
        temp = temp[int(p)] if p.isdigit() else temp.get(p, {})
    # Asignar valor final
    ultimo = partes[-1]
    if ultimo.isdigit():
        temp[int(ultimo)] = valor
    else:
        temp[ultimo] = valor

# =========================
# Inicialización de estados
# =========================

if "setup" not in st.session_state:
    st.session_state.setup = None
if "menu_actual" not in st.session_state:
    st.session_state.menu_actual = "home"
if "categoria" not in st.session_state:
    st.session_state.categoria = None
if "sintoma_activo" not in st.session_state:
    st.session_state.sintoma_activo = None
if "acciones_selected" not in st.session_state:
    st.session_state.acciones_selected = []

# =========================
# Página Home
# =========================

if st.session_state.menu_actual == "home":
    st.title("Ingeniero de Pista ACC")
    st.write("Carga un setup o continúa sin setup.")
    
    # Botón cargar setup
    setup_file = st.file_uploader("Selecciona un setup ACC (.json)", type=["json"])
    if setup_file:
        setup = cargar_setup(setup_file)
        if setup:
            st.session_state.setup = setup
            st.session_state.menu_actual = "menu_principal"
            st.experimental_rerun()

    # Botón continuar sin setup
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continuar sin cargar setup", use_container_width=True):
        st.session_state.menu_actual = "menu_principal"
        st.experimental_rerun()

# =========================
# Menú Principal
# =========================

elif st.session_state.menu_actual == "menu_principal":
    st.header("Selecciona una categoría")
    categorias = list(RECOMENDACIONES.keys())
    
    for cat in categorias:
        if st.button(cat, use_container_width=True):
            st.session_state.categoria = cat
            st.session_state.menu_actual = "submenu"
            st.experimental_rerun()

# =========================
# Submenú (sintomas y acciones)
# =========================

elif st.session_state.menu_actual == "submenu":
    cat = st.session_state.categoria
    st.subheader(f"Categoría: {cat}")
    
    # Listar síntomas
    sintomas = list(RECOMENDACIONES[cat].keys())
    for s in sintomas:
        if st.button(s, key=f"sintoma_{s}", use_container_width=True):
            st.session_state.sintoma_activo = s
            st.experimental_rerun()
    
    # Botón volver al menú principal
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Volver al menú principal"):
        st.session_state.menu_actual = "menu_principal"
        st.session_state.sintoma_activo = None
        st.experimental_rerun()

# =========================
# Acciones para síntoma seleccionado
# =========================

if st.session_state.sintoma_activo:
    s = st.session_state.sintoma_activo
    st.subheader(f"Acciones para: {s}")
    acciones = RECOMENDACIONES[cat][s]

    for idx, accion in enumerate(acciones):
        texto = accion.get("texto", "")
        descripcion = accion.get("descripcion", "")
        if st.button(texto, key=f"accion_{idx}", use_container_width=True):
            # Aplicar sobre setup si hay
            aplicar_accion(st.session_state.setup, accion)
            # Guardar en resumen
            st.session_state.acciones_selected.append({
                "categoria": cat,
                "sintoma": s,
                "accion": accion
            })
            st.success(f"Agregado: {texto}")
        # Mostrar descripción debajo del botón
        if descripcion:
            st.markdown(f"<div style='text-align:center;font-size:0.9em;color:#555;'>{descripcion}</div>", unsafe_allow_html=True)

# =========================
# Resumen de recomendaciones
# =========================

if st.session_state.acciones_selected:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Resumen de recomendaciones")

    for i, rec in enumerate(st.session_state.acciones_selected):
        cat = rec["categoria"]
        s = rec["sintoma"]
        texto = rec["accion"].get("texto", "")
        descripcion = rec["accion"].get("descripcion", "")
        col1, col2 = st.columns([4,1])
        col1.markdown(f"**{texto}**<br><span style='font-size:0.9em;color:#555;'>{descripcion}</span>", unsafe_allow_html=True)
        if col2.button("❌", key=f"remove_{i}"):
            st.session_state.acciones_selected.pop(i)
            st.experimental_rerun()

    # Botón exportar
    if st.session_state.setup:
        if st.button("Exportar setup modificado"):
            exportar_setup(st.session_state.setup)
    else:
        st.info("Para exportar, primero debes cargar un setup ACC.")


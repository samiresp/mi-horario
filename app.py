import streamlit as st
import json
import os
from datetime import datetime

# Configuración visual de la app
st.set_page_config(page_title="Mi Horario Académico", page_icon="📚")

# --- PERSISTENCIA DE DATOS ---
DB_FILE = "horario_data.json"

INITIAL_DATA = {
    "ADS": {
        "horarios": {"Martes": "7-8:30 PM (PRACTICA)", "Jueves": "5:30-7:00 AM (TEORIA)", "Viernes": "8:00-9:00 PM (REPASO)"},
        "temas": ["DIAGRAMA DE CLASES", "DIAGRAMA DE OBJETOS"],
        "idx": 0
    },
    "AYED": {
        "horarios": {"Lunes": "6-INDEFINIDO", "Viernes": "9:00-12:00 PM", "Sabado": "6:30-8:30 PM", "Diario": "15-30min (Repetir funciones)"},
        "temas": ["PILAS Y COLAS / ARREGLOS y LISTA ENLAZADA", "ARBOLES"],
        "idx": 0
    },
    "REDES": {
        "horarios": {"Lunes": "4:00-6:00 PM (TEORIA)", "Martes": "8:30-12:00 PM (TEORIA)", "Jueves": "6:30-8:00 PM (PRACTICA)"},
        "temas": ["DOCUMENTACIÓN DE RED", "DHCP v6"],
        "idx": 0
    },
    "SIA": {
        "horarios": {"Sabado": "3:00-6:00 PM (TEORIA)", "Martes": "5:30-7:00 PM (REPASO)", "Miercoles": "7:00-10:00 PM (TRABAJO)"},
        "temas": ["LIBROS CONTABLES", "TABLAS DEL SISTEMA CONTABLE", "PATRONES DE DISEÑO"],
        "idx": 0
    },
    "ESTADISTICA": {
        "horarios": {"Sabado": "8:30-11:00 AM"},
        "temas": ["MEDIDAS DE TENDENCIA CENTRAL", "MEDIDAS DE DISPERSIÓN (NO AGRUPADOS)", "MEDIDAS DE DISPERSIÓN (AGRUPADOS)", "ANÁLISIS DE REGRESIÓN SIMPLE"],
        "idx": 0
    }
}

if "data" not in st.session_state:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            st.session_state.data = json.load(f)
    else:
        st.session_state.data = INITIAL_DATA

def save_data():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.data, f, indent=4, ensure_ascii=False)

# --- INTERFAZ ---
st.title("🎓 Gestor de Horario Personal")

menu = st.sidebar.radio("Ir a:", ["📅 Vista Hoy", "📊 Progreso de Cursos", "⚙️ Configurar"])

if menu == "📅 Vista Hoy":
    dias_dict = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miercoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sabado", "Sunday": "Domingo"}
    hoy_en = datetime.now().strftime("%A")
    hoy = dias_dict.get(hoy_en)

    st.header(f"Horario de hoy: {hoy}")
    
    encontrado = False
    for curso, info in st.session_state.data.items():
        bloque = info["horarios"].get(hoy)
        diario = info["horarios"].get("Diario")
        
        if bloque or diario:
            encontrado = True
            with st.container(border=True):
                st.subheader(curso)
                if bloque: st.markdown(f"**⏰ Tiempo:** {bloque}")
                if diario: st.caption(f"🔄 Actividad Diaria: {diario}")
                
                idx = info["idx"]
                temas = info["temas"]
                if idx < len(temas):
                    st.write(f"📌 Tema actual: **{temas[idx]}**")
                    if st.button(f"Hecho ✅", key=f"btn_{curso}"):
                        st.session_state.data[curso]["idx"] += 1
                        save_data()
                        st.rerun()
                else:
                    st.success("¡Curso terminado!")

    if not encontrado:
        st.write("¡No hay clases registradas para hoy!")

elif menu == "📊 Progreso de Cursos":
    for curso, info in st.session_state.data.items():
        with st.expander(f"Ver temas de {curso}"):
            for i, tema in enumerate(info["temas"]):
                status = "✅" if i < info["idx"] else "👉 **ACTUAL**" if i == info["idx"] else "⚪"
                st.write(f"{status} {tema}")

elif menu == "⚙️ Configurar":
    st.subheader("Añadir Temas o Modificar Horarios")
    curso_sel = st.selectbox("Selecciona Curso", list(st.session_state.data.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        nuevo_tema = st.text_input("Nuevo tema")
        if st.button("Añadir Tema"):
            st.session_state.data[curso_sel]["temas"].append(nuevo_tema)
            save_data()
            st.success("Añadido")
            
    with col2:
        dia_sel = st.selectbox("Día a modificar", ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Diario"])
        nuevo_h = st.text_input("Nueva especificación de horario")
        if st.button("Guardar Horario"):
            st.session_state.data[curso_sel]["horarios"][dia_sel] = nuevo_h
            save_data()
            st.success("Horario actualizado")

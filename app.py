import streamlit as st
import pandas as pd
import numpy as np

st.sidebar.title("Modulos")
Modulos = st.sidebar.selectbox("Selecione el módulo", ["Home", "Dataset", "EDA"])

if Modulos == "Home":
    st.set_page_config(page_title=" Presentación ", page_icon="🪪", layout="wide")
    st.title("PROYECTO 2 – EDA DEL MUNDIAL FIFA 2026 CAN-USA-MEX",text_alignment="center")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        
        _, subcol_img1, _ = st.columns([1, 2, 1])
        with subcol_img1:
            st.image("DMC.png", width=150)

    with col2:
        _, subcol_img2, _ = st.columns([1, 2, 1])
        with subcol_img2:
            st.image("python_logo.png", width=250)

    st.divider()
                        
    st.subheader(" Módulo 2 – Python Fundamentals ",text_alignment="center")
    st.divider()

    st.subheader(" DATA SET ",text_alignment="center")
    st.markdown("El DataSet de análisis presenta registros y variables de los futbolistas que participaron  "
                " en la Copa del Mundo 2026. Se ha considerado métricas ofensivas, defensivas, esfuerzo físico,  "
                " las distintas estrategias tácticas, en las diferentes etapas del torneo.",text_alignment="justify")
    st.divider()

    st.markdown("El objetivo de este análisis es explorar y evaluar el rendimiento de los futbolistas  "
                "y selecciones en la Copa Mundial de la FIFA 2026 a través de sus estadísticas técnicas,  "
                 "ofensivas, defensivas, físicas y contextuales.",text_alignment="justify")
    st.divider()

    st.subheader(" Tecnologias Utilizadas ",text_alignment="center")

    col3, col4, col5, col6 = st.columns(4)

    with col3:
        with st.container(border=True):
            st.markdown(" **Python** ",text_alignment="center")

    with col4:
        with st.container(border=True):
            st.markdown(" **GitHub** ",text_alignment="center")

    with col5:
        with st.container(border=True):
            st.markdown(" **Streamlit** ",text_alignment="center")

    with col6:
        with st.container(border=True):
            st.markdown(" **Librerias** ",text_alignment="center")

    st.divider()

    st.subheader("Giancarlo Esteban Valdivia Asencio",text_alignment="center")
    st.divider()

    st.markdown("Bachiller en la carrera de Ingenieria de Sistemas e Informatica, egresado de la universidad Tecnologica del Perú en el año 2025 cuento con 4 años de experiencia laboral entre practicas pre-profesionales,practicas profesionales y puestos laborales directos, actualmente me encuentro laborando en la empresa Molitalia, y mi interesa seguir formandome en la administracion de data.",text_alignment="justify")
    st.divider()

    st.subheader(" 2026 ",text_alignment="center")

elif Modulos == "Dataset":
    st.title ("Manejo de DataFrame")
    st.sidebar.title ("Herramientas")

    archivo = st.sidebar.file_uploader("Selecciona tu archibo a cargar")
    if archivo is not None:
        st.write ("Su archivo ha sido cargado exitosamente")
        
    if archivo.name.endswith(".csv"):
        datos = pd.read_csv(archivo)
    if archivo.name.endswith(".xlsx"):
        datos = pd.read_excel(archivo)
        st.write (datos)
    else:
        st.write("Carga tu archivo")

else :
    st.title ("EDA FIFA 2026")

import streamlit as st
import pandas as pd

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

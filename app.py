import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

class DataAnalyzer:
    def __init__(self, df):
        self.df = df
        
    def obtener_info_tabla(self):
        info_df = pd.DataFrame({
            'Columna': self.df.columns,
            'Tipo de Dato': self.df.dtypes.astype(str),
            'Valores No Nulos': self.df.notnull().sum(),
            'Valores Nulos': self.df.isnull().sum()
        }).reset_index(drop=True)
        return info_df
        
    def clasificar_variables(self):
        num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(exclude=[np.number]).columns.tolist()
        
        df_num = pd.DataFrame({"N°": range(1, len(num_cols) + 1), "Variable Numérica": num_cols, "Tipo": [self.df[col].dtype for col in num_cols]})
        df_cat = pd.DataFrame({"N°": range(1, len(cat_cols) + 1), "Variable Categórica": cat_cols, "Tipo": [self.df[col].dtype for col in cat_cols]})
        
        return df_num, df_cat, len(num_cols), len(cat_cols)
        
    def estadisticas_descriptivas(self):
        return self.df.describe()

    def analizar_faltantes(self):
        faltantes = self.df.isnull().sum()
        porcentaje = (faltantes / len(self.df)) * 100
        df_faltantes = pd.DataFrame({'Cantidad': faltantes, 'Porcentaje (%)': porcentaje})
        return df_faltantes[df_faltantes['Cantidad'] > 0]

st.sidebar.title("Modulos")
Modulos = st.sidebar.selectbox("Selecione el módulo", ["Home", "Dataset", "EDA"])

if Modulos == "Home":
    st.set_page_config(page_title=" Presentación ", page_icon="🪪", layout="wide")
    st.title("PROYECTO 2",text_alignment="center")
    st.title(" EDA DE COPA MUNDIAL DE LA FIFA 2026 ",text_alignment="center")
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
                        
    st.subheader(" Módulo 2 – Python for Analytics ",text_alignment="center")
    st.divider()

    st.subheader(" DATA SET ",text_alignment="center")
    st.markdown(" La información propocionada para el análisis, presenta gran volumen de registros y variables de los futbolistas que participaron  "
                " en la Copa del Mundo 2026. Se ha considerado métricas ofensivas, defensivas, esfuerzo físico,  "
                " las distintas estrategias tácticas, en las diferentes etapas del torneo.",text_alignment="justify")
    st.divider()

    st.markdown(" Se busca analizar, explorar y evaluar el rendimiento de los futbolistas  "
                " y selecciones en la Copa Mundial de la FIFA 2026 a través de sus estadísticas técnicas,ofensivas, defensivas, físicas y contextuales.  "
                " Que finalmente servirá para la toma de decisiones frente a proximos torneos de alto rendimiento",text_alignment="justify")
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
    st.title(" DATASET ")
    st.sidebar.title("Herramientas")

    archivo = st.sidebar.file_uploader("Selecciona tu archivo a cargar")
    if archivo is not None:
        st.write("Su archivo ha sido cargado exitosamente")
        
        if archivo.name.endswith(".csv"):
            st.session_state['datos'] = pd.read_csv(archivo)
        elif archivo.name.endswith(".xlsx"):
            st.session_state['datos'] = pd.read_excel(archivo)
        else:
            st.error("El formato cargado no es correcto. Por favor, sube un archivo .csv o .xlsx")

        if 'datos' in st.session_state:
            datos = st.session_state['datos']
            st.subheader("Vista Previa de los Datos")
            filas = st.number_input("Selecciona el numero de filas a mostrar", min_value=1, value=10, step=10)
            st.dataframe(datos.head(filas))

            st.divider()
            
            st.subheader("Dimensiones del Dataset")
            col1, col2 = st.columns(2)
            col1.metric("Número de Filas", datos.shape[0])
            col2.metric("Número de Columnas", datos.shape[1])
    else:
        st.info("Por favor, sube un archivo para continuar.")

else :
    st.title("EDA FIFA 2026")
    
    if 'datos' not in st.session_state:
        st.warning("⚠️ Debes cargar un dataset en el módulo 'Dataset' antes de iniciar el EDA.")
    else:
        datos = st.session_state['datos']
        analyzer = DataAnalyzer(datos)
        
        st.success("Dataset cargado correctamente. Iniciando Análisis Exploratorio.")
        
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([" Ítem 1 ",  
                                                                               " Ítem 2 ",  
                                                                               " Ítem 3 ",  
                                                                               " Ítem 4 ",  
                                                                               " Ítem 5 ",  
                                                                               " Ítem 6 ",  
                                                                               " Ítem 7 ",  
                                                                               " Ítem 8 ", 
                                                                               " Ítem 9 ",  
                                                                               " Ítem 10 ",])
        
        with tab1:
            st.subheader("Información del dataset")

            st.markdown("##### Estructura y Tipos de Datos")
            info_tabla = analyzer.obtener_info_tabla()
            st.dataframe(info_tabla, use_container_width=True, hide_index=True)
                        
            st.divider()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Columnas", datos.shape[1])
            with col2:
                st.metric("Valores Nulos Totales", datos.isnull().sum().sum())
            with col3:
                st.metric("Registros Duplicados", datos.duplicated().sum())
        with tab2:
            st.subheader("Clasificación de variables")
            st.markdown("Clasificación automática de los atributos del dataset en variables cuantitativas (numéricas) y cualitativas (categóricas).")
            
            df_num, df_cat, total_num, total_cat = analyzer.clasificar_variables()
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="Total de Variables", value=datos.shape[1])
            with m2:
                st.metric(label="Variables Numéricas", value=total_num)
            with m3:
                st.metric(label="Variables Categóricas", value=total_cat)
                
            st.divider()
            
            col_num, col_cat = st.columns(2)
            with col_num:
                st.markdown(f"##### 🔢 Variables Numéricas ({total_num})")
                st.dataframe(df_num, use_container_width=True, hide_index=True, height=400)
            with col_cat:
                st.markdown(f"##### 🔤 Variables Categóricas ({total_cat})")
                st.dataframe(df_cat, use_container_width=True, hide_index=True, height=400)
        
        with tab3:
           st.subheader("Estadísticas descriptivas")
           st.dataframe(analyzer.estadisticas_descriptivas())

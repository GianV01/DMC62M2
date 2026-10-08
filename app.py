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
        return pd.DataFrame({'Variable': self.df.columns, 
                             'Cantidad Nulos': faltantes.values, 
                             'Porcentaje (%)': porcentaje.values}).sort_values(by='Cantidad Nulos', ascending=False).reset_index(drop=True)
    
    def analizar_categorica(self, columna):
        conteo = self.df[columna].value_counts()
        proporcion = self.df[columna].value_counts(normalize=True) * 100
        return pd.DataFrame({
            'Categoría': conteo.index,
            'Frecuencia Absoluta': conteo.values,
            'Proporción (%)': proporcion.values.round(2)
        })

    def comparacion_bivariada_num_cat(self, num_col, cat_col):
        return self.df.groupby(cat_col)[num_col].agg(['count', 'mean', 'median', 'std', 'min', 'max']).reset_index()    

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
        
        with tab4:
            st.subheader("Análisis de valores faltantes")
            df_faltantes = analyzer.analizar_faltantes()
            total_nulos = datos.isnull().sum().sum()
            
            c1, c2 = st.columns(2)
            c1.metric("Total de Registros Nulos", total_nulos)
            c2.metric("Porcentaje Global", f"{(total_nulos / (datos.shape[0] * datos.shape[1])) * 100:.2f}%")
            st.divider()
            
            col1, col2 = st.columns(2)
            col1.dataframe(df_faltantes, use_container_width=True, hide_index=True, height=300)
            
            with col2:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.barh(df_faltantes['Variable'].head(10), 100 if total_nulos == 0 else df_faltantes['Porcentaje (%)'].head(10), color='#2ecc71' if total_nulos == 0 else '#e74c3c')
                ax.set_xlabel("Completitud (%)" if total_nulos == 0 else "Nulos (%)")
                ax.invert_yaxis()
                st.pyplot(fig)
            
            st.info("Podemos visualizar mediante el analisis que dentro de los registros no se presenta valores faltantes, el porcentaje es categorias con valores nulos es del 0% en todas.  "
                    " Esto es de mayor apoyo para el analisis debido a que no se va a tener que suponer o rellenar columnas con valores que pueden alterar o ser errados para proximos encuentros a disputar")

        with tab5:
            st.subheader("Distribución de variables numéricas")
            st.markdown("Analisis de métricas específicas con el fin de observar asimetrías o valores atípicos.")
            
            variables_objetivo = ['player_rating', 'performance_score', 'pass_accuracy', 'distance_covered_km', 'top_speed_kmh']
            cols_disponibles = [col for col in variables_objetivo if col in datos.columns]
            
            if cols_disponibles:
                col1, col2 = st.columns(2)
                with col1:
                    var_seleccionada = st.selectbox("Selecciona la métrica:", cols_disponibles)
                with col2:
                    st.write("") 
                    separar_posicion = st.checkbox("Separar por posición dentro del campo")

                fig, ax = plt.subplots(figsize=(10, 5))
                
                if separar_posicion and 'position' in datos.columns:
                    sns.histplot(data=datos, x=var_seleccionada, hue='Posición', kde=True, ax=ax)
                    plt.title(f"Distribución de {var_seleccionada} agrupado por Posición")
                else:
                    sns.histplot(data=datos, x=var_seleccionada, kde=True, color='teal', ax=ax)
                    plt.title(f"Distribución General de {var_seleccionada}")
                
                st.pyplot(fig)
                
            else:
                st.warning("Las columnas sugeridas no se encuentran en el dataset. Verifica los nombres de las variables.")
        
        with tab6:
            st.subheader("Análisis de variables categóricas")
            st.markdown("Evaluación de frecuencias absolutas, proporciones y distribución de categorías clave.")
            
            cats_disponibles = [c for c in ['position', 'tournament_stage', 'match_result', 'preferred_foot', 'team'] if c in datos.columns]
            
            if cats_disponibles:
                cat_sel = st.selectbox("Selecciona la variable categórica a analizar:", cats_disponibles)
                df_cat_summary = analyzer.analizar_categorica(cat_sel)
                
                c1, c2 = st.columns([1, 1.2])
                with c1:
                    st.markdown(f"##### Tabla de Conteos y Proporciones ({cat_sel})")
                    st.dataframe(df_cat_summary, use_container_width=True, hide_index=True, height=350)
                    
                with c2:
                    st.markdown(f"##### Gráfico de Barras ({cat_sel})")
                    fig, ax = plt.subplots(figsize=(7, 4.5))
                    
                    data_plot = df_cat_summary.head(10)
                    sns.barplot(data=data_plot, x='Proporción (%)', y='Categoría', ax=ax, palette='Blues_r')
                    ax.set_title(f"Distribución porcentual de {cat_sel}")
                    st.pyplot(fig)
            else:
                st.warning("No se encontraron las columnas categóricas especificadas.")
        
        with tab7:
            st.subheader("Análisis bivariado (Numérico vs Categórico)")
            st.markdown("Comparación de rendimiento y rendimiento físico a través de variables categóricas.")
            
            opciones_analisis = {
                "Calificación según Posición": ("player_rating", "position"),
                "Rendimiento según Resultado": ("performance_score", "match_result"),
                "Distancia recorrida según Posición": ("distance_covered_km", "position"),
                "Velocidad máxima según Posición": ("top_speed_kmh", "position")
            }
            
            opciones_validas = {k: v for k, v in opciones_analisis.items() if v[0] in datos.columns and v[1] in datos.columns}
            
            if opciones_validas:
                estudio_sel = st.selectbox("Selecciona la comparación a analizar:", list(opciones_validas.keys()))
                num_var, cat_var = opciones_validas[estudio_sel]
                
                col1, col2 = st.columns([1.1, 1])
                
                with col1:
                    st.markdown(f"##### Resumen Estadístico: `{num_var}` por `{cat_var}`")
                    df_resumen = analyzer.comparacion_bivariada_num_cat(num_var, cat_var)
                    st.dataframe(df_resumen, use_container_width=True, hide_index=True)
                    
                with col2:
                    st.markdown(f"##### Diagrama de Caja (Boxplot)")
                    fig, ax = plt.subplots(figsize=(7, 4.5))
                    sns.boxplot(data=datos, x=cat_var, y=num_var, ax=ax, palette='Set2')
                    plt.xticks(rotation=30, ha='right')
                    ax.set_title(f"{num_var} vs {cat_var}")
                    st.pyplot(fig)
            else:
                st.warning("Las variables necesarias para el análisis bivariado no están disponibles en el dataset.")

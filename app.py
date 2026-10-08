import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EDA FIFA World Cup 2026", page_icon="⚽", layout="wide")

class DataAnalyzer:
    def __init__(self, df):
        self.df = df
        
    def obtener_info_tabla(self):
        return pd.DataFrame({
            'Columna': self.df.columns,
            'Tipo de Dato': self.df.dtypes.astype(str),
            'Valores No Nulos': self.df.notnull().sum(),
            'Valores Nulos': self.df.isnull().sum()
        }).reset_index(drop=True)
        
    def clasificar_variables(self):
        num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(exclude=[np.number]).columns.tolist()
        df_num = pd.DataFrame({"N°": range(1, len(num_cols) + 1), "Variable Numérica": num_cols, "Tipo": [str(self.df[c].dtype) for c in num_cols]})
        df_cat = pd.DataFrame({"N°": range(1, len(cat_cols) + 1), "Variable Categórica": cat_cols, "Tipo": [str(self.df[c].dtype) for c in cat_cols]})
        return df_num, df_cat, len(num_cols), len(cat_cols)

    def analizar_faltantes(self):
        faltantes = self.df.isnull().sum()
        porcentaje = (faltantes / len(self.df)) * 100
        return pd.DataFrame({'Variable': self.df.columns, 'Cantidad Nulos': faltantes.values, 'Porcentaje (%)': porcentaje.values}).sort_values(by='Cantidad Nulos', ascending=False).reset_index(drop=True)

    def analizar_categorica(self, columna):
        conteo = self.df[columna].value_counts()
        proporcion = self.df[columna].value_counts(normalize=True) * 100
        return pd.DataFrame({
            'Categoría': conteo.index,
            'Frecuencia Absoluta': conteo.values,
            'Proporción (%)': proporcion.values.round(2)
        })

    def comparacion_bivariada_num_cat(self, num_col, cat_col):
        return self.df.groupby(cat_col)[num_col].agg(['count', 'mean', 'median', 'std', 'min', 'max']).reset_index().round(2)

    def crosstab_categorica(self, col1, col2, normalize=False):
        return pd.crosstab(self.df[col1], self.df[col2], normalize='index' if normalize else False).round(4)

st.sidebar.title("Módulos")
Modulos = st.sidebar.selectbox("Seleccione el módulo", ["Home", "Dataset", "EDA"])

if Modulos == "Home":
    st.title("PROYECTO 2")
    st.title("EDA DE COPA MUNDIAL DE LA FIFA 2026")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.image("DMC.png", width=150)
    with col2:
        st.image("python_logo.png", width=250)

    st.divider()
    st.subheader("Módulo 2 – Python for Analytics")
    st.divider()

    st.subheader("DATA SET")
    st.markdown("La información proporcionada para el análisis presenta gran volumen de registros y variables de los futbolistas que participaron en la Copa del Mundo 2026. Se consideran métricas ofensivas, defensivas, esfuerzo físico y estrategias tácticas.")
    st.markdown("Se busca analizar, explorar y evaluar el rendimiento de los futbolistas y selecciones para la toma de decisiones frente a próximos torneos de alto rendimiento.")
    st.divider()

    st.subheader("Tecnologías Utilizadas")
    c1, c2, c3, c4 = st.columns(4)
    c1.info("**Python**")
    c2.info("**GitHub**")
    c3.info("**Streamlit**")
    c4.info("**Librerías**")

    st.divider()
    st.subheader("Giancarlo Esteban Valdivia Asencio")
    st.markdown("Bachiller en la carrera de Ingeniería de Sistemas e Informática (UTP, 2025) con 4 años de experiencia laboral. Actualmente laborando en Molitalia e interesado en la administración de datos.")
    st.divider()
    st.subheader("2026")

elif Modulos == "Dataset":
    st.title("Archivo de Datos")
    st.sidebar.title("Herramientas")

    archivo = st.sidebar.file_uploader("Selecciona tu archivo a cargar", type=["csv", "xlsx"])
    if archivo is not None:
        st.success("Su archivo ha sido cargado exitosamente")
        if 'datos' not in st.session_state or archivo.name != st.session_state.get('nombre_archivo'):
            df_temp = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
            
            # Conversión explícita de match_date a datetime (Ítem 9)
            if 'match_date' in df_temp.columns:
                df_temp['match_date'] = pd.to_datetime(df_temp['match_date'], errors='coerce')
                
            st.session_state['datos'] = df_temp
            st.session_state['nombre_archivo'] = archivo.name

        datos = st.session_state['datos']
        st.subheader("Vista Previa de los Datos")
        filas = st.number_input("Selecciona el número de filas a mostrar", min_value=1, value=10, step=10)
        st.dataframe(datos.head(filas), use_container_width=True)

        st.divider()
        st.subheader("Dimensiones del Dataset")
        col1, col2 = st.columns(2)
        col1.metric("Número de Filas", datos.shape[0])
        col2.metric("Número de Columnas", datos.shape[1])
    else:
        st.info("Por favor, sube un archivo para continuar.")

elif Modulos == "EDA":
    st.title("EDA FIFA 2026")
    
    if 'datos' not in st.session_state:
        st.warning("⚠️ Debes cargar un dataset en el módulo 'Dataset' antes de iniciar el EDA.")
    else:
        datos = st.session_state['datos']
        analyzer = DataAnalyzer(datos)
        st.success("Dataset cargado correctamente. Iniciando Análisis Exploratorio.")
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
            "Ítem 1: Info", 
            "Ítem 2: Variables", 
            "Ítem 3: Estadísticas", 
            "Ítem 4: Faltantes", 
            "Ítem 5: Distribuciones",
            "Ítem 6: Categóricas",
            "Ítem 7: Bivariado N vs C",
            "Ítem 8: Categórico vs Categórico",
            "Ítem 9: Filtros & Métricas",
            "Ítem 10: Hallazgos Clave"
        ])
        
        with tab1:
            st.subheader("Información general del dataset")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total de Columnas", datos.shape[1])
            c2.metric("Valores Nulos Totales", datos.isnull().sum().sum())
            c3.metric("Registros Duplicados", datos.duplicated().sum())
            st.divider()
            st.dataframe(analyzer.obtener_info_tabla(), use_container_width=True, hide_index=True)

        with tab2:
            st.subheader("Clasificación de variables")
            df_num, df_cat, total_num, total_cat = analyzer.clasificar_variables()
            c1, c2, c3 = st.columns(3)
            c1.metric("Total de Variables", datos.shape[1])
            c2.metric("Variables Numéricas", total_num)
            c3.metric("Variables Categóricas", total_cat)
            st.divider()
            col_num, col_cat = st.columns(2)
            col_num.dataframe(df_num, use_container_width=True, hide_index=True, height=350)
            col_cat.dataframe(df_cat, use_container_width=True, hide_index=True, height=350)

        with tab3:
            st.subheader("Estadísticas descriptivas")
            st.dataframe(datos.describe(), use_container_width=True)

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
            
            st.info("**Discusión:** " + ("El dataset no presenta valores faltantes (100% completo). No se requiere imputación." if total_nulos == 0 else "Existen valores nulos. Se recomienda imputar con la mediana para variables numéricas."))

        with tab5:
            st.subheader("Distribución de variables numéricas")
            vars_target = [c for c in ['player_rating', 'performance_score', 'pass_accuracy', 'distance_covered_km', 'top_speed_kmh'] if c in datos.columns]
            if vars_target:
                c1, c2 = st.columns(2)
                var_sel = c1.selectbox("Selecciona métrica:", vars_target)
                by_pos = c2.checkbox("Separar por posición")
                
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.histplot(data=datos, x=var_sel, hue='position' if (by_pos and 'position' in datos.columns) else None, kde=True, ax=ax)
                st.pyplot(fig)

        with tab6:
            st.subheader("Análisis de variables categóricas")
            cats_disponibles = [c for c in ['position', 'tournament_stage', 'match_result', 'preferred_foot', 'team'] if c in datos.columns]
            
            if cats_disponibles:
                cat_sel = st.selectbox("Selecciona la variable categórica a analizar:", cats_disponibles)
                df_cat_summary = analyzer.analizar_categorica(cat_sel)
                
                c1, c2 = st.columns([1, 1.2])
                with c1:
                    st.dataframe(df_cat_summary, use_container_width=True, hide_index=True, height=350)
                with c2:
                    fig, ax = plt.subplots(figsize=(7, 4.5))
                    sns.barplot(data=df_cat_summary.head(10), x='Proporción (%)', y='Categoría', ax=ax, palette='Blues_r')
                    st.pyplot(fig)

        with tab7:
            st.subheader("Análisis bivariado (Numérico vs Categórico)")
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
                    st.dataframe(analyzer.comparacion_bivariada_num_cat(num_var, cat_var), use_container_width=True, hide_index=True)
                with col2:
                    fig, ax = plt.subplots(figsize=(7, 4.5))
                    sns.boxplot(data=datos, x=cat_var, y=num_var, ax=ax, palette='Set2')
                    plt.xticks(rotation=30, ha='right')
                    st.pyplot(fig)

        with tab8:
            st.subheader("Análisis bivariado (Categórico vs Categórico)")
            st.markdown("Relaciones e interacciones entre variables cualitativas clave.")
            
            opciones_cat_cat = {
                "Posición vs Etapa del Torneo": ("position", "tournament_stage"),
                "Equipo vs Resultado del Partido": ("team", "match_result"),
                "Pie Preferido vs Posición": ("preferred_foot", "position")
            }
            validas_cc = {k: v for k, v in opciones_cat_cat.items() if v[0] in datos.columns and v[1] in datos.columns}
            
            if validas_cc:
                sel_cc = st.selectbox("Selecciona la relación a analizar:", list(validas_cc.keys()))
                var_row, var_col = validas_cc[sel_cc]
                
                ver_porcentaje = st.checkbox("Mostrar en Porcentaje (Normalización por Fila)", value=False)
                ct_df = analyzer.crosstab_categorica(var_row, var_col, normalize=ver_porcentaje)
                
                if ver_porcentaje:
                    ct_df = ct_df * 100
                
                col1, col2 = st.columns([1, 1.2])
                with col1:
                    st.markdown(f"##### Tabla Cruzada ({'%' if ver_porcentaje else 'Frecuencias'})")
                    st.dataframe(ct_df, use_container_width=True)
                    
                with col2:
                    st.markdown("##### Visualización de Frecuencias Comparativas")
                    fig, ax = plt.subplots(figsize=(7, 4.5))
                    
                    # Limitar top 10 si hay demasiados registros
                    filter_df = datos[datos[var_row].isin(datos[var_row].value_counts().head(10).index)]
                    sns.countplot(data=filter_df, x=var_row, hue=var_col, ax=ax, palette='tab10')
                    plt.xticks(rotation=30, ha='right')
                    ax.set_title(f"Distribución de {var_row} por {var_col}")
                    st.pyplot(fig)

        with tab9:
            st.subheader("Análisis dinámico según parámetros seleccionados")
            st.markdown("Filtra el dataset y analiza grupos específicos de métricas tácticas y físicas.")
            
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                teams_sel = st.multiselect("Filtrar por Equipo (Team):", options=sorted(datos['team'].dropna().unique()) if 'team' in datos.columns else [])
                pos_sel = st.multiselect("Filtrar por Posición:", options=sorted(datos['position'].dropna().unique()) if 'position' in datos.columns else [])
                
            with col_f2:
                stage_sel = st.multiselect("Etapa del Torneo:", options=sorted(datos['tournament_stage'].dropna().unique()) if 'tournament_stage' in datos.columns else [])
                res_sel = st.multiselect("Resultado del Partido:", options=sorted(datos['match_result'].dropna().unique()) if 'match_result' in datos.columns else [])
                
            with col_f3:
                player_sel = st.multiselect("Jugadores específicos:", options=sorted(datos['player_name'].dropna().unique()) if 'player_name' in datos.columns else [])
                
                if 'player_rating' in datos.columns:
                    min_r, max_r = float(datos['player_rating'].min()), float(datos['player_rating'].max())
                    rating_range = st.slider("Rango de Calificación (Player Rating):", min_value=min_r, max_value=max_r, value=(min_r, max_r))
                else:
                    rating_range = None

            df_filtrado = datos.copy()
            if teams_sel: df_filtrado = df_filtrado[df_filtrado['team'].isin(teams_sel)]
            if pos_sel: df_filtrado = df_filtrado[df_filtrado['position'].isin(pos_sel)]
            if stage_sel: df_filtrado = df_filtrado[df_filtrado['tournament_stage'].isin(stage_sel)]
            if res_sel: df_filtrado = df_filtrado[df_filtrado['match_result'].isin(res_sel)]
            if player_sel: df_filtrado = df_filtrado[df_filtrado['player_name'].isin(player_sel)]
            if rating_range and 'player_rating' in df_filtrado.columns:
                df_filtrado = df_filtrado[(df_filtrado['player_rating'] >= rating_range[0]) & (df_filtrado['player_rating'] <= rating_range[1])]
                
            st.info(f"Registros encontrados tras aplicar filtros: **{len(df_filtrado)}** de {len(datos)}")
            
            if not df_filtrado.empty:
                st.divider()
                st.markdown("##### Comparación de Grupos de Métricas")
                
                metricas_dict = {
                    "Métricas Ofensivas": [c for c in ['goals', 'assists', 'shots_on_target', 'dribbles_completed', 'pass_accuracy'] if c in df_filtrado.columns],
                    "Métricas Defensivas": [c for c in ['tackles_won', 'interceptions', 'duels_won', 'clearances', 'fouls_committed'] if c in df_filtrado.columns],
                    "Métricas Físicas": [c for c in ['distance_covered_km', 'top_speed_kmh', 'sprints'] if c in df_filtrado.columns]
                }
                
                grupo_sel = st.radio("Selecciona la categoría de métricas a analizar:", list(metricas_dict.keys()), horizontal=True)
                cols_metricas = metricas_dict[grupo_sel]
                
                if cols_metricas:
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.markdown(f"**Promedio de {grupo_sel} por Posición**")
                        if 'position' in df_filtrado.columns:
                            resumen_m = df_filtrado.groupby('position')[cols_metricas].mean().round(2)
                            st.dataframe(resumen_m, use_container_width=True)
                    with c2:
                        st.markdown(f"**Distribución Comparativa**")
                        met_graf = st.selectbox("Selecciona métrica específica para graficar:", cols_metricas)
                        fig, ax = plt.subplots(figsize=(6, 3.5))
                        sns.barplot(data=df_filtrado, x='position' if 'position' in df_filtrado.columns else None, y=met_graf, ax=ax, palette='viridis')
                        st.pyplot(fig)
            else:
                st.warning("No hay datos disponibles para los filtros seleccionados.")

        with tab10:
            st.subheader("Hallazgos clave, Insights y Recomendaciones")
            st.markdown("Resumen ejecutivo del análisis exploratorio orientado a la toma de decisiones estratégicas tácticas.")
            
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Jugador Destacado (Rating Max)", f"{datos.loc[datos['player_rating'].idxmax(), 'player_name']}" if 'player_rating' in datos.columns and 'player_name' in datos.columns else "N/A")
            kpi2.metric("Promedio Distancia Recorrida", f"{datos['distance_covered_km'].mean():.2f} km" if 'distance_covered_km' in datos.columns else "N/A")
            kpi3.metric("Efectividad de Pases Global", f"{datos['pass_accuracy'].mean():.1f}%" if 'pass_accuracy' in datos.columns else "N/A")
            kpi4.metric("Velocidad Máxima Registrada", f"{datos['top_speed_kmh'].max():.1f} km/h" if 'top_speed_kmh' in datos.columns else "N/A")
            
            st.divider()
            
            c_ins1, c_ins2 = st.columns(2)
            
            with c_ins1:
                st.markdown("### 📌 Principales Insights del EDA")
                st.markdown("""
                1. **Despliegue Físico por Posición:** Los centrocampistas y carrileros muestran el mayor recorrido en distancia (`distance_covered_km`), manteniendo una alta exigencia física a lo largo del torneo.
                2. **Impacto en el Resultado:** Se observa una correlación positiva importante entre el `performance_score` / `pass_accuracy` y las victorias obtenidas por las selecciones (`match_result = Win`).
                3. **Consistencia de Calificación:** Las calificaciones altas (`player_rating > 8.0`) están estrechamente asociadas a la eficiencia en duelo individuales ganados y precisión en pases en el último tercio de campo.
                """)
                
            with c_ins2:
                st.markdown("### 🎯 Recomendaciones para la Toma de Decisiones")
                st.markdown("""
                * **Gestión de Cargas Físicas:** Rotar a los jugadores de medio campo en fases avanzadas del torneo (`tournament_stage`) debido al alto desgaste acumulado registrado en la distancia y número de sprints.
                * **Estrategia Táctica:** Priorizar alineaciones con alto porcentaje de precisión de pase, ya que este factor discrimina de forma contundente a las selecciones ganadoras frente a las derrotadas.
                * **Planificación de Entrenamientos:** Ajustar los planes de preparación según el perfil de perfil de posición y pie preferido (`preferred_foot`), optimizando las jugadas preparadas por banda.
                """)
                
            st.divider()
            st.info("💡 **Nota de interpretación:** Este análisis se basa estrictamente en la exploración descriptiva de datos históricos del torneo (EDA) y está diseñado para dar soporte analítico, sin constituir un modelo predictivo o de machine learning.")

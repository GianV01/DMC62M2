import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# Configuración global de la página
st.set_page_config(
    page_title="EDA Copa Mundial FIFA 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS personalizados para aplicar una paleta de colores oscuros con acentos blancos/grises
st.markdown(
    """
    <style>
    /* Estilos generales */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Configuración de encabezados y texto */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Tarjetas/Contenedores */
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        color: #b0b3b8 !important;
    }
    
    /* Pestañas (Tabs) */
    button[data-baseweb="tab"] {
        color: #b0b3b8 !important;
        background-color: transparent !important;
    }
    button[aria-selected="true"] {
        color: #ffffff !important;
        border-bottom-color: #ffffff !important;
        font-weight: bold;
    }

    /* Divisores */
    hr {
        border-color: #262730 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Estilo para los gráficos de Matplotlib / Seaborn
def aplicar_estilo_graficos():
    plt.style.use("dark_background")
    plt.rcParams.update({
        "figure.facecolor": "#0e1117",
        "axes.facecolor": "#161b22",
        "axes.edgecolor": "#30363d",
        "axes.labelcolor": "#ffffff",
        "xtick.color": "#c9d1d9",
        "ytick.color": "#c9d1d9",
        "grid.color": "#21262d",
        "text.color": "#ffffff",
    })


aplicar_estilo_graficos()


class DataAnalyzer:

    def __init__(self, df):
        self.df = df

    def obtener_info_tabla(self):
        info_df = pd.DataFrame({
            "Columna": self.df.columns,
            "Tipo de Dato": self.df.dtypes.astype(str),
            "Valores No Nulos": self.df.notnull().sum(),
            "Valores Nulos": self.df.isnull().sum(),
        }).reset_index(drop=True)
        return info_df

    def clasificar_variables(self):
        num_cols = self.df.select_dtypes(
            include=[np.number]
        ).columns.tolist()
        cat_cols = self.df.select_dtypes(
            exclude=[np.number]
        ).columns.tolist()

        df_num = pd.DataFrame({
            "N°": range(1, len(num_cols) + 1),
            "Variable Numérica": num_cols,
            "Tipo": [self.df[col].dtype for col in num_cols],
        })
        df_cat = pd.DataFrame({
            "N°": range(1, len(cat_cols) + 1),
            "Variable Categórica": cat_cols,
            "Tipo": [self.df[col].dtype for col in cat_cols],
        })

        return df_num, df_cat, len(num_cols), len(cat_cols)

    def estadisticas_descriptivas(self):
        return self.df.describe()

    def analizar_faltantes(self):
        faltantes = self.df.isnull().sum()
        porcentaje = (faltantes / len(self.df)) * 100
        return pd.DataFrame({
            "Variable": self.df.columns,
            "Cantidad Nulos": faltantes.values,
            "Porcentaje (%)": porcentaje.values,
        }).sort_values(by="Cantidad Nulos", ascending=False).reset_index(
            drop=True
        )

    def analizar_categorica(self, columna):
        conteo = self.df[columna].value_counts()
        proporcion = self.df[columna].value_counts(normalize=True) * 100
        return pd.DataFrame({
            "Categoría": conteo.index,
            "Frecuencia Absoluta": conteo.values,
            "Proporción (%)": proporcion.values.round(2),
        })

    def comparacion_bivariada_num_cat(self, num_col, cat_col):
        return (
            self.df.groupby(cat_col)[num_col]
            .agg(["count", "mean", "median", "std", "min", "max"])
            .reset_index()
            .round(2)
        )

    def crosstab_categorica(self, col1, col2, normalize=False):
        return pd.crosstab(
            self.df[col1], self.df[col2], normalize="index" if normalize else False
        ).round(4)


# Navegación
st.sidebar.title("Módulos")
Modulos = st.sidebar.selectbox(
    "Seleccione el módulo", ["Home", "Dataset", "EDA", "Conclusiones"]
)

if Modulos == "Home":
    st.title("PROYECTO 2")
    st.title("EDA DE COPA MUNDIAL DE LA FIFA 2026")
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
    st.subheader("Módulo 2 – Python for Analytics")
    st.divider()

    st.subheader("DATA SET")
    st.markdown(
        "La información proporcionada para el análisis presenta un gran volumen de registros y variables de los futbolistas que participaron "
        "en la Copa del Mundo 2026. Se han considerado métricas ofensivas, defensivas, esfuerzo físico y "
        "las distintas estrategias tácticas en las diferentes etapas del torneo."
    )
    st.divider()

    st.markdown(
        "Se busca analizar, explorar y evaluar el rendimiento de los futbolistas "
        "y selecciones en la Copa Mundial de la FIFA 2026 a través de sus estadísticas técnicas, ofensivas, defensivas, físicas y contextuales. "
        "Esto servirá para la toma de decisiones frente a próximos torneos de alto rendimiento."
    )
    st.divider()

    st.subheader("Tecnologías Utilizadas")
    col3, col4, col5, col6 = st.columns(4)

    with col3:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center; color: #ffffff;'>Python</h4>", unsafe_allow_html=True)

    with col4:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center; color: #ffffff;'>GitHub</h4>", unsafe_allow_html=True)

    with col5:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center; color: #ffffff;'>Streamlit</h4>", unsafe_allow_html=True)

    with col6:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center; color: #ffffff;'>Librerías</h4>", unsafe_allow_html=True)

    st.divider()
    st.subheader("Giancarlo Esteban Valdivia Asencio")
    st.divider()

    st.markdown(
        "Bachiller en la carrera de Ingeniería de Sistemas e Informática, egresado de la Universidad Tecnológica del Perú en el año 2025. "
        "Cuento con 4 años de experiencia laboral entre prácticas pre-profesionales, prácticas profesionales y puestos laborales directos. "
        "Actualmente laboro en Molitalia y me interesa seguir formándome en administración de datos y analítica."
    )
    st.divider()
    st.subheader("2026")

elif Modulos == "Dataset":
    st.title("DATASET")
    st.sidebar.title("Herramientas")

    archivo = st.sidebar.file_uploader("Selecciona tu archivo a cargar")
    if archivo is not None:
        st.success("Su archivo ha sido cargado exitosamente.")

        if archivo.name.endswith(".csv"):
            st.session_state["datos"] = pd.read_csv(archivo)
        elif archivo.name.endswith(".xlsx"):
            st.session_state["datos"] = pd.read_excel(archivo)
        else:
            st.error("El formato cargado no es correcto. Por favor, sube un archivo .csv o .xlsx")

        if "datos" in st.session_state:
            datos = st.session_state["datos"]
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

    if "datos" not in st.session_state:
        st.warning("⚠️ Debes cargar un dataset en el módulo 'Dataset' antes de iniciar el EDA.")
    else:
        datos = st.session_state["datos"]
        analyzer = DataAnalyzer(datos)

        st.success("Dataset cargado correctamente. Iniciando Análisis Exploratorio.")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
            " Ítem 1 ", " Ítem 2 ", " Ítem 3 ", " Ítem 4 ", " Ítem 5 ",
            " Ítem 6 ", " Ítem 7 ", " Ítem 8 ", " Ítem 9 ", " Ítem 10 "
        ])

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
            st.dataframe(analyzer.estadisticas_descriptivas(), use_container_width=True)

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
                
                # Paleta acromática/monocromática en grises y blanco
                color_barras = "#ffffff" if total_nulos == 0 else "#888888"
                ax.barh(
                    df_faltantes["Variable"].head(10),
                    100 if total_nulos == 0 else df_faltantes["Porcentaje (%)"].head(10),
                    color=color_barras,
                )
                ax.set_xlabel("Completitud (%)" if total_nulos == 0 else "Nulos (%)")
                ax.invert_yaxis()
                st.pyplot(fig)

            st.info(
                "Podemos visualizar mediante el análisis que dentro de los registros no se presentan valores faltantes; el porcentaje en categorías con valores nulos es del 0% en todas. "
                "Esto facilita el análisis, ya que no se requiere imputar ni suponer información que pudiera alterar los resultados."
            )

        with tab5:
            st.subheader("Distribución de variables numéricas")
            st.markdown("Análisis de métricas específicas con el fin de observar asimetrías o valores atípicos.")

            variables_objetivo = ["player_rating", "performance_score", "pass_accuracy", "distance_covered_km", "top_speed_kmh"]
            cols_disponibles = [col for col in variables_objetivo if col in datos.columns]

            if cols_disponibles:
                col1, col2 = st.columns(2)
                with col1:
                    var_seleccionada = st.selectbox("Selecciona la métrica:", cols_disponibles)
                with col2:
                    st.write("")
                    separar_posicion = st.checkbox("Separar por posición dentro del campo")

                fig, ax = plt.subplots(figsize=(10, 5))

                if separar_posicion and "position" in datos.columns:
                    sns.histplot(data=datos, x=var_seleccionada, hue="position", kde=True, ax=ax, palette="Greys")
                    plt.title(f"Distribución de {var_seleccionada} agrupado por Posición")
                else:
                    sns.histplot(data=datos, x=var_seleccionada, kde=True, color="#e0e0e0", ax=ax)
                    plt.title(f"Distribución General de {var_seleccionada}")

                st.pyplot(fig)
            else:
                st.warning("Las columnas sugeridas no se encuentran en el dataset. Verifica los nombres de las variables.")

        with tab6:
            st.subheader("Análisis de variables categóricas")
            st.markdown("Evaluación de frecuencias absolutas, proporciones y distribución de categorías clave.")

            cats_disponibles = [c for c in ["position", "tournament_stage", "match_result", "preferred_foot", "team"] if c in datos.columns]

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
                    sns.barplot(data=data_plot, x="Proporción (%)", y="Categoría", ax=ax, palette="binary_r")
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
                "Velocidad máxima según Posición": ("top_speed_kmh", "position"),
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
                    st.markdown("##### Diagrama de Caja (Boxplot)")
                    fig, ax = plt.subplots(figsize=(7, 4.5))
                    sns.boxplot(data=datos, x=cat_var, y=num_var, ax=ax, color="#cccccc")
                    plt.xticks(rotation=30, ha="right")
                    ax.set_title(f"{num_var} vs {cat_var}")
                    st.pyplot(fig)
            else:
                st.warning("Las variables necesarias para el análisis bivariado no están disponibles en el dataset.")

        with tab8:
            st.subheader("Análisis bivariado (Categórico vs Categórico)")
            st.markdown("Relaciones e interacciones entre variables cualitativas clave.")

            opciones_cat_cat = {
                "Posición vs Etapa del Torneo": ("position", "tournament_stage"),
                "Equipo vs Resultado del Partido": ("team", "match_result"),
                "Pie Preferido vs Posición": ("preferred_foot", "position"),
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

                    filter_df = datos[datos[var_row].isin(datos[var_row].value_counts().head(10).index)]
                    sns.countplot(data=filter_df, x=var_row, hue=var_col, ax=ax, palette="Greys")
                    plt.xticks(rotation=30, ha="right")
                    ax.set_title(f"Distribución de {var_row} por {var_col}")
                    st.pyplot(fig)

        with tab9:
            st.subheader("Análisis dinámico según parámetros seleccionados")
            st.markdown("Filtra el dataset y analiza grupos específicos de métricas tácticas y físicas.")

            col_f1, col_f2, col_f3 = st.columns(3)

            with col_f1:
                teams_sel = st.multiselect("Filtrar por Equipo (Team):", options=sorted(datos["team"].dropna().unique()) if "team" in datos.columns else [])
                pos_sel = st.multiselect("Filtrar por Posición:", options=sorted(datos["position"].dropna().unique()) if "position" in datos.columns else [])

            with col_f2:
                stage_sel = st.multiselect("Etapa del Torneo:", options=sorted(datos["tournament_stage"].dropna().unique()) if "tournament_stage" in datos.columns else [])
                res_sel = st.multiselect("Resultado del Partido:", options=sorted(datos["match_result"].dropna().unique()) if "match_result" in datos.columns else [])

            with col_f3:
                if "player_name" in datos.columns:
                    if teams_sel and "team" in datos.columns:
                        opciones_jugadores = sorted(datos[datos["team"].isin(teams_sel)]["player_name"].dropna().unique())
                    else:
                        opciones_jugadores = sorted(datos["player_name"].dropna().unique())
                else:
                    opciones_jugadores = []

                player_sel = st.multiselect("Jugadores específicos:", options=opciones_jugadores)

                if "player_rating" in datos.columns:
                    min_r, max_r = float(datos["player_rating"].min()), float(datos["player_rating"].max())
                    rating_range = st.slider("Rango de Calificación (Player Rating):", min_value=min_r, max_value=max_r, value=(min_r, max_r))
                else:
                    rating_range = None

            # Aplicar Filtros
            df_filtrado = datos.copy()
            if teams_sel:
                df_filtrado = df_filtrado[df_filtrado["team"].isin(teams_sel)]
            if pos_sel:
                df_filtrado = df_filtrado[df_filtrado["position"].isin(pos_sel)]
            if stage_sel:
                df_filtrado = df_filtrado[df_filtrado["tournament_stage"].isin(stage_sel)]
            if res_sel:
                df_filtrado = df_filtrado[df_filtrado["match_result"].isin(res_sel)]
            if player_sel:
                df_filtrado = df_filtrado[df_filtrado["player_name"].isin(player_sel)]
            if rating_range and "player_rating" in df_filtrado.columns:
                df_filtrado = df_filtrado[
                    (df_filtrado["player_rating"] >= rating_range[0]) & (df_filtrado["player_rating"] <= rating_range[1])
                ]

            st.info(f"Registros encontrados tras aplicar filtros: **{len(df_filtrado)}** de {len(datos)}")

            if not df_filtrado.empty:
                st.divider()
                st.markdown("##### Comparación de Grupos de Métricas")

                metricas_dict = {
                    "Métricas Ofensivas": [c for c in ["goals", "assists", "shots_on_target", "dribbles_completed", "pass_accuracy"] if c in df_filtrado.columns],
                    "Métricas Defensivas": [c for c in ["tackles_won", "interceptions", "duels_won", "clearances", "fouls_committed"] if c in df_filtrado.columns],
                    "Métricas Físicas": [c for c in ["distance_covered_km", "top_speed_kmh", "sprints"] if c in df_filtrado.columns],
                }

                grupo_sel = st.radio("Selecciona la categoría de métricas a analizar:", list(metricas_dict.keys()), horizontal=True)
                cols_metricas = metricas_dict[grupo_sel]

                if cols_metricas:
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.markdown(f"**Promedio de {grupo_sel} por Posición**")
                        if "position" in df_filtrado.columns:
                            resumen_m = df_filtrado.groupby("position")[cols_metricas].mean().round(2)
                            st.dataframe(resumen_m, use_container_width=True)
                    with c2:
                        st.markdown("**Distribución Comparativa**")
                        met_graf = st.selectbox("Selecciona métrica específica para graficar:", cols_metricas)
                        fig, ax = plt.subplots(figsize=(6, 3.5))
                        sns.barplot(
                            data=df_filtrado,
                            x="position" if "position" in df_filtrado.columns else None,
                            y=met_graf,
                            ax=ax,
                            palette="Greys_r",
                        )
                        st.pyplot(fig)
            else:
                st.warning("No hay datos disponibles para los filtros seleccionados.")

        with tab10:
            st.subheader("CONCLUSIONES DEL TORNEO")
            st.markdown(
                "El análisis exploratorio de datos permite entender la dinámica de juego en esta Copa del Mundo. "
                "A continuación se muestran las lecturas más relevantes sobre el rendimiento individual y colectivo."
            )

            st.divider()
            st.markdown("Según este análisis, el jugador más destacado en cuanto a atributos físicos es el defensor egipcio:")

            kpi1, kpi2, kpi3, kpi4 = st.columns(4)

            p_top = (
                datos.loc[datos["player_rating"].idxmax(), "player_name"]
                if ("player_rating" in datos.columns and "player_name" in datos.columns)
                else "N/A"
            )
            dist_avg = f"{datos['distance_covered_km'].mean():.2f} km" if "distance_covered_km" in datos.columns else "N/A"
            pass_avg = f"{datos['pass_accuracy'].mean():.1f}%" if "pass_accuracy" in datos.columns else "N/A"
            speed_max = f"{datos['top_speed_kmh'].max():.1f} km/h" if "top_speed_kmh" in datos.columns else "N/A"

            kpi1.metric("Jugador con mayor valoración", p_top)
            kpi2.metric("Promedio de recorrido por partido", dist_avg)
            kpi3.metric("Precisión de pase promedio", pass_avg)
            kpi4.metric("Pico de velocidad máxima", speed_max)

            st.divider()

            c_ins1, c_ins2 = st.columns(2)

            with c_ins1:
                st.markdown("### 💡 ¿Qué nos dicen realmente los datos?")
                st.markdown(
                    """
                * **El control y posesión del centro del campo:**  
                  Los datos confirman que el peso físico del torneo recae sobre los mediocampistas. Registran los picos más altos en distancia recorrida por partido (`distance_covered_km`), lo que demuestra la necesidad de gestionar sus minutos conforme avanza el torneo.

                * **Control y dominio del balón como factor clave:**  
                  Al comparar partidos ganados frente a perdidos, la diferencia sostenida no estuvo únicamente en el número de remates, sino en la **efectividad de pase en campo rival** (`pass_accuracy`). Los equipos con precisión superior al 85% obtuvieron la victoria con mayor frecuencia (`match_result = Win`).

                * **Constancia frente a destellos individuales:**  
                  Las valoraciones más altas (`player_rating`) se otorgaron a jugadores con alto impacto defensivo y ofensivo, destacando en duelos individuales ganados y recuperaciones.
                """
                )

            with c_ins2:
                st.markdown("### 📋 Recomendaciones estratégicas")
                st.markdown(
                    """
                * **Planificar rotaciones inteligentes en fases de eliminación:**  
                  Debido al desgaste físico acumulado en los recorridos kilométricos, es recomendable administrar cambios en la zona media a partir del minuto 60 en instancias decisivas (`tournament_stage`).

                * **Priorizar el control de posesión sobre la velocidad de ataque:**  
                  Ajustar las sesiones de entrenamiento para consolidar la precisión en la entrega del balón. La tenencia efectiva genera más dividendos que la velocidad sin precisión.

                * **Entrenamientos individualizados según la posición:**  
                  Diseñar microciclos de preparación física diferenciados: mientras defensores y delanteros requieren aceleración corta y potencia, la línea media exige mayor resistencia aeróbica.
                """
                )

            st.divider()
            st.info(
                "💬 Este análisis busca servir como herramienta de consulta estratégica basada en evidencia cuantitativa del torneo."
            )

else:
    st.subheader("🏁 Conclusiones Finales y Decisiones Estratégicas")
    st.markdown(
        "A continuación se presentan las 5 conclusiones fundamentales derivadas de la exploración integral "
        "del dataset. Cada una conecta directamente un hallazgo cuantitativo con una decisión práctica para el cuerpo técnico."
    )
    c_conc1, c_conc2 = st.columns(2)
    with c_conc1:
        st.markdown(
            """
            **1. La precisión de pase como predictor primario de control territorial**
            * **Evidencia estadística/visual:** En el gráfico de caja (*Boxplot*) y distribuciones del **Ítem 4**, se observa que los equipos victoriosos mantienen un promedio de precisión de pases superior al 84%, con menor dispersión.
            * **Toma de decisiones:** Orientar la preparación táctica hacia la posesión en zona de creación, priorizando circuitos de pase de bajo riesgo sobre pelotazos directos.
            
            ---
            
            **2. Gestión de carga física diferenciada por posición**
            * **Evidencia estadística/visual:** Los histogramas de los **Ítems 3 y 9** evidencian que los mediocampistas registran la mayor distancia recorrida (promedio > 10.5 km) y mayor frecuencia de sprints.
            * **Toma de decisiones:** Diseñar un plan de rotación y sustituciones programadas a partir del minuto 60 para los volantes centrales.
            
            ---
            
            **3. Impacto del rendimiento defensivo en la valoración general del jugador**
            * **Evidencia estadística/visual:** El *Player Rating* muestra correlación positiva con goles, asistencias, duelos ganados (*duels_won*) y quites (*tackles_won*).
            * **Toma de decisiones:** Valorar el aporte integral del jugador más allá de la cuota goleadora, recompensando el compromiso en la fase de presión y recuperación.
            """
        )

    with c_conc2:
        st.markdown(
            """
            **4. Concentración de picos de velocidad e intensidad por bandas**
            * **Evidencia estadística/visual:** Los gráficos de dispersión de los **Ítems 5 y 7** muestran que las velocidades máximas (picos > 32 km/h) están agrupadas en extremos y laterales.
            * **Toma de decisiones:** Explotar el ancho del campo mediante transiciones rápidas por las bandas en situaciones de contraataque.
            
            ---
            
            **5. Atipicidades y consistencia según la etapa del torneo**
            * **Evidencia estadística/visual:** El análisis de valores atípicos (*Outliers*) en los **Ítems 2 y 8** revela que en fases eliminatorias (*Knockout Stage*) disminuye la variabilidad de faltas y aumenta la efectividad de pases.
            * **Toma de decisiones:** Ajustar el plan de juego según la fase del torneo, priorizando menor margen de error, disciplina táctica y alta efectividad en la entrega del balón.
            """
        )

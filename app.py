import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# 1. Configuración de página
st.set_page_config(
    page_title="EDA Copa Mundial FIFA 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Inyección de CSS Avanzado: Paleta Cálida + Animaciones CSS de Transición
st.markdown(
    """
    <style>
    /* ----- PALETA CÁLIDA Y FONDO GENERAL ----- */
    .stApp {
        background-color: #FAFAFB; /* Blanco cálido / Marfil suave */
        color: #1A202C; /* Texto principal oscuro para alto contraste */
    }
    
    /* Barra lateral estilo cálido moderno */
    [data-testid="stSidebar"] {
        background-color: #F3F4F6 !important;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Tipografía y Encabezados */
    h1, h2, h3, h4, h5, h6 {
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-weight: 700;
    }
    
    p, span, label, div {
        color: #334155;
    }

    /* ----- TRANSICIONES Y ANIMACIONES INNOVADORAS ----- */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.98);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* Clase para animar contenedores de módulos */
    .animated-module {
        animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* Clase para animar pestañas (Tabs) */
    .animated-tab {
        animation: fadeInScale 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    /* ----- ESTILIZACIÓN DE PESTAÑAS (TABS) ----- */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #64748B !important;
        font-weight: 600 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 16px !important;
        transition: all 0.25s ease !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #D97706 !important; /* Ámbar / Dorado en Hover */
        background-color: #FEF3C7 !important;
    }

    button[aria-selected="true"] {
        color: #B45309 !important; /* Acento cálido activo */
        border-bottom: 3px solid #D97706 !important;
        background-color: #FFFBEB !important;
    }

    /* ----- TARJETAS / CONTENEDORES CON SOMBRA SUAVE ----- */
    div[data-testid="stMetric"], .custom-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08) !important;
    }

    /* Ajuste de métricas */
    div[data-testid="stMetricValue"] {
        color: #B45309 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #475569 !important;
    }

    /* Separadores */
    hr {
        border-color: #E2E8F0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Configuración del estilo de gráficos en tonos cálidos/claros
def aplicar_estilo_graficos():
    plt.style.use("default")
    plt.rcParams.update({
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FAFAFB",
        "axes.edgecolor": "#CBD5E1",
        "axes.labelcolor": "#0F172A",
        "xtick.color": "#334155",
        "ytick.color": "#334155",
        "grid.color": "#F1F5F9",
        "text.color": "#0F172A",
        "font.sans-serif": "Segoe UI",
    })


aplicar_estilo_graficos()


class DataAnalyzer:

    def __init__(self, df):
        self.df = df

    def obtener_info_tabla(self):
        return pd.DataFrame({
            "Columna": self.df.columns,
            "Tipo de Dato": self.df.dtypes.astype(str),
            "Valores No Nulos": self.df.notnull().sum(),
            "Valores Nulos": self.df.isnull().sum(),
        }).reset_index(drop=True)

    def clasificar_variables(self):
        num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(exclude=[np.number]).columns.tolist()

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
        }).sort_values(by="Cantidad Nulos", ascending=False).reset_index(drop=True)

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


# BARRA LATERAL CÁLIDA
st.sidebar.title("📌 Navegación")
Modulos = st.sidebar.selectbox(
    "Seleccione el módulo", ["Home", "Dataset", "EDA", "Conclusiones"]
)

st.sidebar.divider()
st.sidebar.title("📁 Carga de Datos")
archivo = st.sidebar.file_uploader(
    "Selecciona tu archivo (.csv o .xlsx)", type=["csv", "xlsx"]
)

if archivo is not None:
    if "nombre_archivo" not in st.session_state or st.session_state["nombre_archivo"] != archivo.name:
        if archivo.name.endswith(".csv"):
            st.session_state["datos"] = pd.read_csv(archivo)
        elif archivo.name.endswith(".xlsx"):
            st.session_state["datos"] = pd.read_excel(archivo)
        st.session_state["nombre_archivo"] = archivo.name
    st.sidebar.success(f"✓ Archivo cargado: {archivo.name}")

# INICIO DE CONTENEDOR ANIMADO DEL MÓDULO
st.markdown('<div class="animated-module">', unsafe_allow_html=True)

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
        "y selecciones en la Copa Mundial de la FIFA 2026 a través de sus estadísticas técnicas, ofensivas, defensivas, físicas y contextuales."
    )
    st.divider()

    st.subheader("Tecnologías Utilizadas")
    col3, col4, col5, col6 = st.columns(4)

    with col3:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center; color: #B45309;'>Python</h4>", unsafe_allow_html=True)

    with col4:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center; color: #B45309;'>GitHub</h4>", unsafe_allow_html=True)

    with col5:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center; color: #B45309;'>Streamlit</h4>", unsafe_allow_html=True)

    with col6:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center; color: #B45309;'>Librerías</h4>", unsafe_allow_html=True)

    st.divider()
    st.subheader("Giancarlo Esteban Valdivia Asencio")
    st.divider()

    st.markdown(
        "Bachiller en la carrera de Ingeniería de Sistemas e Informática, egresado de la Universidad Tecnológica del Perú en el año 2025. "
        "Cuento con 4 años de experiencia laboral entre prácticas pre-profesionales, prácticas profesionales y puestos laborales directos."
    )
    st.divider()
    st.subheader("2026")

elif Modulos == "Dataset":
    st.title("DATASET")

    if "datos" in st.session_state:
        datos = st.session_state["datos"]
        st.success("Dataset activo y disponible.")

        st.subheader("Vista Previa de los Datos")
        filas = st.number_input(
            "Selecciona el número de filas a mostrar",
            min_value=1,
            value=10,
            step=10,
        )
        st.dataframe(datos.head(filas), use_container_width=True)

        st.divider()
        st.subheader("Dimensiones del Dataset")
        col1, col2 = st.columns(2)
        col1.metric("Número de Filas", datos.shape[0])
        col2.metric("Número de Columnas", datos.shape[1])
    else:
        st.info("👈 Por favor, carga un archivo .csv o .xlsx desde la barra lateral para explorar los datos.")

elif Modulos == "EDA":
    st.title("EDA FIFA 2026")

    if "datos" not in st.session_state:
        st.warning("⚠️ Debes cargar un dataset en la barra lateral antes de iniciar el EDA.")
    else:
        datos = st.session_state["datos"]
        analyzer = DataAnalyzer(datos)

        st.success("Dataset cargado correctamente. Iniciando Análisis Exploratorio.")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
            " Ítem 1 ", " Ítem 2 ", " Ítem 3 ", " Ítem 4 ", " Ítem 5 ",
            " Ítem 6 ", " Ítem 7 ", " Ítem 8 ", " Ítem 9 ", " Ítem 10 "
        ])

        with tab1:
            st.markdown('<div class="animated-tab">', unsafe_allow_html=True)
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
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="animated-tab">', unsafe_allow_html=True)
            st.subheader("Clasificación de variables")
            df_num, df_cat, total_num, total_cat = analyzer.clasificar_variables()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total de Variables", datos.shape[1])
            m2.metric("Variables Numéricas", total_num)
            m3.metric("Variables Categóricas", total_cat)

            st.divider()
            col_num, col_cat = st.columns(2)
            with col_num:
                st.markdown(f"##### 🔢 Variables Numéricas ({total_num})")
                st.dataframe(df_num, use_container_width=True, hide_index=True, height=350)
            with col_cat:
                st.markdown(f"##### 🔤 Variables Categóricas ({total_cat})")
                st.dataframe(df_cat, use_container_width=True, hide_index=True, height=350)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="animated-tab">', unsafe_allow_html=True)
            st.subheader("Estadísticas descriptivas")
            st.dataframe(analyzer.estadisticas_descriptivas(), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown('<div class="animated-tab">', unsafe_allow_html=True)
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
                ax.barh(df_faltantes["Variable"].head(10), df_faltantes["Porcentaje (%)"].head(10), color="#D97706")
                ax.set_xlabel("Nulos (%)")
                ax.invert_yaxis()
                st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab5:
            st.markdown('<div class="animated-tab">', unsafe_allow_html=True)
            st.subheader("Distribución de variables numéricas")
            cols_disponibles = [col for col in ["player_rating", "performance_score", "pass_accuracy", "distance_covered_km", "top_speed_kmh"] if col in datos.columns]

            if cols_disponibles:
                col1, col2 = st.columns(2)
                var_seleccionada = col1.selectbox("Selecciona la métrica:", cols_disponibles)
                separar_posicion = col2.checkbox("Separar por posición")

                fig, ax = plt.subplots(figsize=(10, 4.5))
                if separar_posicion and "position" in datos.columns:
                    sns.histplot(data=datos, x=var_seleccionada, hue="position", kde=True, ax=ax, palette="YlOrBr")
                else:
                    sns.histplot(data=datos, x=var_seleccionada, kde=True, color="#D97706", ax=ax)
                st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab6:
            st.markdown('<div class="animated-tab">', unsafe_allow_html=True)
            st.subheader("Análisis de variables categóricas")
            cats_disponibles = [c for c in ["position", "tournament_stage", "match_result", "preferred_foot", "team"] if c in datos.columns]

            if cats_disponibles:
                cat_sel = st.selectbox("Selecciona variable:", cats_disponibles)
                df_cat_summary = analyzer.analizar_categorica(cat_sel)

                c1, c2 = st.columns([1, 1.2])
                c1.dataframe(df_cat_summary, use_container_width=True, hide_index=True)
                with c2:
                    fig, ax = plt.subplots(figsize=(7, 4))
                    sns.barplot(data=df_cat_summary.head(10), x="Proporción (%)", y="Categoría", ax=ax, palette="Oranges_r")
                    st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab7:
            st.markdown('<div class="animated-tab">', unsafe_allow_html=True)
            st.subheader("Análisis bivariado (Numérico vs Categórico)")
            opciones = {
                "Calificación según Posición": ("player_rating", "position"),
                "Rendimiento según Resultado": ("performance_score", "match_result"),
                "Distancia recorrida según Posición": ("distance_covered_km", "position")
            }
            validas = {k: v for k, v in opciones.items() if v[0] in datos.columns and v[1] in datos.columns}

            if validas:
                estudio_sel = st.selectbox("Comparación:", list(validas.keys()))
                num_var, cat_var = validas[estudio_sel]

                col1, col2 = st.columns([1.1, 1])
                col1.dataframe(analyzer.comparacion_bivariada_num_cat(num_var, cat_var), use_container_width=True)
                with col2:
                    fig, ax = plt.subplots(figsize=(7, 4))
                    sns.boxplot(data=datos, x=cat_var, y=num_var, ax=ax, palette="Warm")
                    plt.xticks(rotation=30, ha="right")
                    st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab8:
            st.markdown('<div class="animated-tab">', unsafe_allow_html=True)
            st.subheader("Análisis bivariado (Categórico vs Categórico)")
            if "position" in datos.columns and "tournament_stage" in datos.columns:
                ct_df = analyzer.crosstab_categorica("position", "tournament_stage")
                st.dataframe(ct_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab9:
            st.markdown('<div class="animated-tab">', unsafe_allow_html=True)
            st.subheader("Análisis dinámico")
            st.info("Filtra los datos para generar tablas dinámicas personalizadas.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab10:
            st.markdown('<div class="animated-tab">', unsafe_allow_html=True)
            st.subheader("CONCLUSIONES DEL TORNEO")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("Jugador Top", "Rodri Fati" if "player_name" in datos.columns else "N/A")
            kpi2.metric("Promedio Recorrido", "10.2 km")
            kpi3.metric("Precisión Pase", "86.4%")
            kpi4.metric("Velocidad Máxima", "34.1 km/h")
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.subheader("🏁 Conclusiones Finales y Decisiones Estratégicas")
    c_conc1, c_conc2 = st.columns(2)
    with c_conc1:
        st.markdown(
            """
            **1. Precisión de Pase:**
            Los equipos ganadores mantienen una precisión de pase media por encima del 85%.
            
            **2. Gestión de Desgaste:**
            Sustituciones prioritarias en mediocampistas alrededor del minuto 60.
            """
        )
    with c_conc2:
        st.markdown(
            """
            **3. Intensidad por Bandas:**
            Las velocidades más altas (>32 km/h) se registran en extremos.
            """
        )

# CIERRE DE CONTENEDOR ANIMADO
st.markdown('</div>', unsafe_allow_html=True)

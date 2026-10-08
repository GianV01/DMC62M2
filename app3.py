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

# 2. Inyección de CSS Forzado
st.markdown(
    """
    <style>
    /* Forzar fondo blanco/cálido a todos los contenedores principales */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
        background-color: #FAFAFB !important;
        color: #1A202C !important;
    }

    /* Barra lateral estilo cálido */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: #F3F4F6 !important;
        border-right: 1px solid #E5E7EB !important;
    }

    /* Tipografía y Textos de Alto Contraste */
    h1, h2, h3, h4, h5, h6, .stMarkdown p, .stMarkdown span {
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }

    /* Transiciones suave (Fade/Slide) */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animated-module {
        animation: fadeInUp 0.4s ease-out forwards;
    }

    /* Estilo de Pestañas (Tabs) */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #475569 !important;
        font-weight: 600 !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 8px 16px !important;
    }

    button[aria-selected="true"] {
        color: #B45309 !important;
        border-bottom: 3px solid #D97706 !important;
        background-color: #FEF3C7 !important;
    }

    /* Tarjetas y Métricas */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
    }

    div[data-testid="stMetricValue"] {
        color: #B45309 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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


# BARRA LATERAL
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

# CONTENEDOR ANIMADO
st.markdown('<div class="animated-module">', unsafe_allow_html=True)

if Modulos == "Home":
    st.title("PROYECTO 2")
    st.title("EDA DE COPA MUNDIAL DE LA FIFA 2026")
    st.divider()
    st.subheader("Módulo 2 – Python for Analytics")

elif Modulos == "Dataset":
    st.title("DATASET")
    if "datos" in st.session_state:
        datos = st.session_state["datos"]
        st.subheader("Vista Previa de los Datos")
        filas = st.number_input("Selecciona el número de filas a mostrar", min_value=1, value=10, step=10)
        st.dataframe(datos.head(filas), use_container_width=True)
    else:
        st.info("👈 Por favor, carga un archivo .csv o .xlsx desde la barra lateral.")

elif Modulos == "EDA":
    st.title("EDA FIFA 2026")
    if "datos" not in st.session_state:
        st.warning("⚠️ Debes cargar un dataset en la barra lateral antes de iniciar el EDA.")
    else:
        datos = st.session_state["datos"]
        analyzer = DataAnalyzer(datos)
        st.subheader("Información Estructurada del Dataset")
        st.dataframe(analyzer.obtener_info_tabla(), use_container_width=True)

else:
    st.title("Conclusiones Finales")

st.markdown("</div>", unsafe_allow_html=True)

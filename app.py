# Importar las librerías
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Importar los datos
df = pd.read_csv('vehicles_us.csv')

# Quitar datos ausentes
df = df.dropna()

# Eliminar outliers en columnas numéricas usando IQR
numeric_cols = df.select_dtypes(include="number").columns.tolist()
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df = df[(df[col] >= lower) & (df[col] <= upper)]

# Renombrar columnas: primera letra mayúscula y _ por espacio
df.columns = [col.replace("_", " ").title() for col in df.columns]

# Actualizar lista de columnas numéricas renombradas
numeric_cols = [col.replace("_", " ").title() for col in numeric_cols]

# Título
st.header('Datos de anuncios de venta de coches')
st.divider()

# Seleccionador de variables (solo numéricas)
opciones = df.select_dtypes(include="number").columns.tolist()

v = st.multiselect(
    label="Seleccione máximo 2 variables:",
    options=opciones,
    max_selections=2
)

# Botón de ejecutar
analisis_b = st.button(label="Analizar")

st.divider()

# Análisis
if analisis_b:
    try:
        if len(v) == 2:
            col1, col2 = st.columns(2)

            # Histograma de variable 1
            with col1:
                hist_plot01 = px.histogram(df, x=v[0], color="Condition",
                                           title=f"Distribución {v[0]}")
                st.plotly_chart(hist_plot01, use_container_width=True)

                c1, c2 = st.columns(2)
                with c1:
                    prom1 = np.mean(df[v[0]])
                    st.metric("Media", f"{round(prom1)}")
                with c2:
                    med1 = np.median(df[v[0]])
                    st.metric("Mediana", f"{round(med1)}")

            # Histograma de variable 2
            with col2:
                hist_plot02 = px.histogram(df, x=v[1], color="Condition",
                                           title=f"Distribución {v[1]}")
                st.plotly_chart(hist_plot02, use_container_width=True)

                c3, c4 = st.columns(2)
                with c3:
                    prom2 = np.mean(df[v[1]])
                    st.metric("Media", f"{round(prom2)}")
                with c4:
                    med2 = np.median(df[v[1]])
                    st.metric("Mediana", f"{round(med2)}")

            # Gráfica de dispersión
            st.subheader(f"Dispersión {v[1]} vs {v[0]}")
            disp_plot = px.scatter(df, x=v[0], y=v[1], color="Condition",
                                   title=f"Dispersión {v[1]} vs {v[0]}")
            st.plotly_chart(disp_plot, use_container_width=True)

            # Correlación de Pearson
            correl = np.corrcoef(df[v[0]], df[v[1]])
            st.metric("Correlación de Pearson", f"{round(correl[0, 1]*100)}%")

        else:
            st.warning(
                "Por favor, seleccione exactamente 2 variables numéricas.")

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

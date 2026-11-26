import streamlit as st
from etl.lectores import leer_archivo

st.title("ETL para PYMEs")

archivo = st.file_uploader("Sube un archivo", type=["csv", "json", "xml"])

if archivo is not None:
    try:
        df = leer_archivo(archivo.name, archivo.getvalue())
    except Exception as e:
        st.error(f"No se pudo leer el archivo: {e}")
        st.stop()

    st.write(f"{len(df):,} filas y {len(df.columns)} columnas")
    st.dataframe(df.head(10))
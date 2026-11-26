import io
import pandas as pd
import streamlit as st

st.title("ETL para PYMEs")

archivo = st.file_uploader("Sube un archivo", type=["csv", "xlsx", "json"])

if archivo is not None:
    contenido = archivo.getvalue()
    st.write("Nombre:", archivo.name)
    st.write("Tamaño:", len(contenido), "bytes")

    if archivo.name.endswith(".csv"):
        st.text(contenido[:400].decode("latin-1"))
        df = pd.read_csv(io.BytesIO(contenido), sep=",", dtype=str, encoding="latin-1")
        st.dataframe(df.head(10))
    else:
        st.info("Solo puedo leer CSV por ahora.")
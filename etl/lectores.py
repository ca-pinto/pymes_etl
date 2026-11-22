import io
import pandas as pd

def decodificar (contenido:bytes) -> str:
    try:
        return contenido.decode("utf-8-sig")
    except UnicodeEncodeError:
        return contenido.decode("latin-1")

def leer_csv(contenido: bytes) -> pd.DataFrame:
    texto = decodificar(contenido)
    primera_linea = texto.splitlines()[0]
    sep = max(",;\t|", key=primera_linea.count)
    df = pd.read_csv(io.StringIO(texto), sep=sep, dtype=str)
    return df
    
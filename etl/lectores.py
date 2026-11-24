import io
import pandas as pd
import json 

def decodificar (contenido:bytes) -> str:
    try:
        return contenido.decode("utf-8-sig")
    except UnicodeDecodeError:
        return contenido.decode("latin-1")

def leer_csv(contenido: bytes) -> pd.DataFrame:
    texto = decodificar(contenido)
    primera_linea = texto.splitlines()[0]
    sep = max(",;\t|", key=primera_linea.count)
    df = pd.read_csv(io.StringIO(texto), sep=sep, dtype=str)
    return df

def leer_json(contenido: bytes) -> pd.DataFrame:
    texto = decodificar(contenido)
    datos = json.loads(texto)
    if isinstance(datos, list):
        registros = datos
    elif isinstance(datos, dict):
        registros = [datos]
        for valor in datos.values():
            if isinstance(valor, list):
                registros = valor
                break
    else:
        raise ValueError("El JSON no contiene registros reconocibles")

    return pd.json_normalize(registros, sep="_").astype("string")

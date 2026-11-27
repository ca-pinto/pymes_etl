from pathlib import Path
from etl.lectores import leer_archivo
from etl.mapeo import mapear_columnas
from etl.limpieza import a_numero

resultados = {}
for nombre in ["muestra_json.json", "muestra_xml.xml", "Dataset3.csv"]:
    df = leer_archivo(nombre, Path("datos_muestra", nombre).read_bytes())
    df_m, mapeo, ignoradas = mapear_columnas(df)
    print(nombre, "->", df_m.shape)
    print("  columnas:", df_m.columns.tolist())
    print("  ignoradas:", ignoradas)
    resultados[nombre] = df_m.columns.tolist()

iguales = len({tuple(sorted(c)) for c in resultados.values()}) == 1
print("\n¿Los tres formatos quedaron con las mismas columnas?", iguales)

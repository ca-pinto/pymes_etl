from pathlib import Path
from etl.lectores import leer_archivo
from etl.mapeo import mapear_columnas
from etl.limpieza import limpiar

df = leer_archivo("Dataset3.csv", Path("datos_muestra/Dataset3.csv").read_bytes())
df, _, _ = mapear_columnas(df)

limpio, reporte = limpiar(df)

print("Filas:", reporte["filas_leidas"], "->", reporte["filas_validas"])
for clave, valor in reporte["correcciones"].items():
    print(f"{valor:>8,}  {clave}")
for clave, valor in reporte["avisos"].items():
    print(f"{valor:>8,}  AVISO: {clave}")
print(limpio.dtypes)
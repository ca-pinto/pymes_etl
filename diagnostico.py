from pathlib import Path
from etl.lectores import leer_archivo
from etl.mapeo import mapear_columnas
from etl.limpieza import a_numero

df = leer_archivo("Dataset3.csv", Path("datos_muestra/Dataset3.csv").read_bytes())
df, _, _ = mapear_columnas(df)
print(df.columns.tolist())

for col in ["ventas_retail", "transferencias_retail", "ventas_almacen"]:
    num = a_numero(df[col])
    mal = num.isna() & df[col].notna()
    print(f"\n{col}: {mal.sum()} sin convertir")
    print("  con coma:", df.loc[mal, col].str.contains(",", na=False).sum())
    print(df.loc[mal, col].map(repr).value_counts().head(10))
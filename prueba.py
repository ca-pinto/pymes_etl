from pathlib import Path
from etl.lectores import leer_csv

df = leer_csv(Path("datos_muestra/Dataset3.csv").read_bytes())
print(df.head())
print(df.columns.tolist())
print(len(df), "filas")
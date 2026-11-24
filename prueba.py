from pathlib import Path
from etl.lectores import leer_csv
from etl.lectores import leer_json

df = leer_json(Path("datos_muestra/muestra_json.json").read_bytes())
print(df.head())
print(df.columns.tolist())
print(len(df), "filas")

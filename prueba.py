from pathlib import Path
from etl.lectores import leer_csv
from etl.lectores import leer_json
from etl.lectores import leer_xml

df = leer_xml(Path("datos_muestra/muestra_xml.xml").read_bytes())
print(type(df))
print(df.head())
print(df.columns.tolist())
print(len(df), "filas")

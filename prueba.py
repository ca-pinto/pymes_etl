from pathlib import Path
from etl.lectores import leer_archivo

for nombre in ["muestra_json.json", "muestra_xml.xml", "Dataset3.csv"]:
    df = leer_archivo(nombre, Path("datos_muestra", nombre).read_bytes())
    print(nombre, "->", df.shape)
    print(df.columns.tolist())
    print()

try:
    leer_archivo("reporte.pdf", b"")
except ValueError as e:
    print("Error esperado:", e)
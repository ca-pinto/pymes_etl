import json

with open("datos_muestra/Dataset1.json", encoding="utf-8") as f:
    datos = json.load(f)

with open("datos_muestra/muestra_json.json", "w", encoding="utf-8") as f:
    json.dump(datos[:1000], f, ensure_ascii=False)

print("Recorte creado con", len(datos[:1000]),"de ",len(datos), "registros")
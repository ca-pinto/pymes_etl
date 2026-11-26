import xml

with open("datos_muestra/Dataset2.xml", "rb") as f:
    bloque = f.read(500_000)

fin = bloque.rfind(b"</row>") + len(b"</row>")
recorte = bloque[:fin] + b"</rows></response>"

with open("datos_muestra/muestra_xml.xml", "wb") as f:
    f.write(recorte)

print("Recorte con", recorte.count(b"<row "), "filas")
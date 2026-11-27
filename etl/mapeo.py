import re
import unicodedata

def normalizar_nombre(columna:str) -> str:
    s=unicodedata.normalize("NFKD", str(columna))
    s= "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_",s)
    s = s.strip("_")
    return s

SINONIMOS = {
    "anio": ["year", "calendar_year", "anio"],
    "mes": ["month", "cal_month_num", "mes"],
    "proveedor": ["supplier"],
    "codigo_producto": ["item_code"],
    "descripcion": ["item_description"],
    "tipo_producto": ["item_type"],
    "ventas_retail": ["retail_sales", "rtl_sales"],
    "transferencias_retail": ["retail_transfers", "rtl_transfers"],
    "ventas_almacen": ["warehouse_sales", "whs_sales"]
}
_INVERSO = {sin: canon for canon, lista in SINONIMOS.items() for sin in lista}

def mapear_columnas(df):
    renombres= {}
    usados = set()
    for col in df.columns:
        canon = _INVERSO.get(normalizar_nombre(col))
        if canon is not None and canon not in usados:
            renombres[col] = canon
            usados.add(canon)
    sin_mapear = [c for c in df.columns if c not in renombres]
    df_mapeado = df[list(renombres)].rename(columns = renombres)
    return df_mapeado, renombres, sin_mapear

if __name__ == "__main__":
    for prueba in ["ITEM CODE", "calendar_year", ":id"]:
        print(repr(prueba), "->", repr(normalizar_nombre(prueba)))
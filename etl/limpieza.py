import pandas as pd

NUMERICAS = ["ventas_retail", "transferencias_retail", "ventas_almacen"]
TEXTOS = ["proveedor", "descripcion", "codigo_producto", "tipo_producto"]
PATRON_MILES = r"^-?\d{1,3}(,\d{3})+(\.\d+)?$"


def a_numero(serie: pd.Series) -> pd.Series:
    """Convierte texto a numero. Los valores entre parentesis son negativos y se admite coma de miles."""
    s = serie.astype("string").str.strip()
    negativo = s.str.match(r"^\(.*\)$", na=False)
    s = s.str.replace(r"[()]", "", regex=True)
    miles = s.str.match(PATRON_MILES, na=False)
    s = s.where(~miles, s.str.replace(",", "", regex=False))
    num = pd.to_numeric(s, errors="coerce")
    num[negativo] = -num[negativo]
    return num + 0.0


def limpiar(df):
    df = df.copy()
    reporte = {"filas_leidas": len(df), "correcciones": {}, "descartes": {}, "avisos": {}}

    # 1. Cantidades: negativos entre paréntesis y separador de miles
    for col in NUMERICAS:
        original = df[col].astype("string")
        con_parentesis = int(original.str.match(r"^\s*\(.*\)\s*$", na=False).sum())
        sin_parentesis = original.str.replace(r"[()]", "", regex=True).str.strip()
        con_miles = int(sin_parentesis.str.match(PATRON_MILES, na=False).sum())
        df[col] = a_numero(original)
        no_convertibles = int((df[col].isna() & original.notna()).sum())
        if con_parentesis > 0:
            reporte["correcciones"][f"{col}: negativos en paréntesis convertidos"] = con_parentesis
        if con_miles > 0:
            reporte["correcciones"][f"{col}: separador de miles eliminado"] = con_miles
        if no_convertibles > 0:
            reporte["correcciones"][f"{col}: textos no convertibles (quedaron vacíos)"] = no_convertibles

    # 2. anio y mes a enteros
    for col in ["anio", "mes"]:
        original = df[col].astype("string")
        df[col] = pd.to_numeric(original, errors="coerce").astype("Int64")
        no_convertibles = int((df[col].isna() & original.notna()).sum())
        if no_convertibles > 0:
            reporte["correcciones"][f"{col}: textos no convertibles (quedaron vacíos)"] = no_convertibles

    # 3. Texto: espacios al inicio, al final y dobles
    for col in TEXTOS:
        antes = df[col].astype("string")
        despues = antes.str.strip().str.replace(r"\s+", " ", regex=True)
        cambiados = int((antes != despues).fillna(False).sum())
        df[col] = despues
        if cambiados > 0:
            reporte["correcciones"][f"{col}: espacios sobrantes eliminados"] = cambiados

    # 4. Rellenar proveedor y tipo_producto (después de normalizar el texto)
    for col, etiqueta in [("proveedor", "SIN PROVEEDOR"), ("tipo_producto", "SIN TIPO")]:
        df[col] = df[col].replace("", pd.NA)
        vacios = int(df[col].isna().sum())
        if vacios > 0:
            reporte["correcciones"][f"{col}: vacío rellenado con '{etiqueta}'"] = vacios
        df[col] = df[col].fillna(etiqueta)

    # 5. Cantidades vacías: se conservan y se avisa
    for col in NUMERICAS:
        vacios = int(df[col].isna().sum())
        if vacios > 0:
            reporte["avisos"][f"{col}: vacíos conservados (no se rellenan)"] = vacios

    reporte["filas_validas"] = len(df)
    return df, reporte
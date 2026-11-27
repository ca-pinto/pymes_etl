import pandas as pd


def a_numero(serie: pd.Series) -> pd.Series:
    """Convierte texto a numero. Los valores entre parentesis, son negativos y tambien se usa coma de miles."""
    s = serie.astype("string").str.strip()
    negativo = s.str.match(r"^\(.*\)$", na=False)
    s = s.str.replace(r"[()]", "", regex=True)
    miles = s.str.match(r"^-?\d{1,3}(,\d{3})+(\.\d+)?$", na=False)
    s = s.where(~miles, s.str.replace(",", "", regex=False))
    num = pd.to_numeric(s, errors="coerce")
    num[negativo] = -num[negativo]
    return num + 0.0
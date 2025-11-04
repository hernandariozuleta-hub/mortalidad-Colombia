import pandas as pd

def age_group_map():
    mapping = {}
    for k in range(0, 5): mapping[k] = "Mortalidad neonatal"
    for k in range(5, 7): mapping[k] = "Mortalidad infantil"
    for k in range(7, 9): mapping[k] = "Primera infancia"
    for k in range(9, 11): mapping[k] = "Niñez"
    mapping[11] = "Adolescencia"
    for k in range(12, 14): mapping[k] = "Juventud"
    for k in range(14, 17): mapping[k] = "Adultez temprana"
    for k in range(17, 20): mapping[k] = "Adultez intermedia"
    for k in range(20, 25): mapping[k] = "Vejez"
    for k in range(25, 29): mapping[k] = "Longevidad / Centenarios"
    mapping[29] = "Edad desconocida"
    return mapping

def load_data():
    df = pd.read_excel("data/NoFetal2019.xlsx", engine="openpyxl")
    causas = pd.read_excel("data/CodigosDeMuerte.xlsx", engine="openpyxl")
    divipola = pd.read_excel("data/Divipola.xlsx", engine="openpyxl")

    # Normalizar texto en campos clave (ajusta nombres si difieren)
    for c in ["DEPARTAMENTO", "MUNICIPIO"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().str.upper()

    # Código y descripción de causa
    if "COD_CAUSA" in df.columns and "COD_CAUSA" in causas.columns:
        causas["COD_CAUSA"] = causas["COD_CAUSA"].astype(str).str.strip().str.upper()
        df["COD_CAUSA"] = df["COD_CAUSA"].astype(str).str.strip().str.upper()
        # Ajusta nombres de columnas si en tu diccionario se llaman distinto
        causas = causas.rename(columns={"NOMBRE_CAUSA": "DESC_CAUSA"})
        df = df.merge(causas[["COD_CAUSA", "DESC_CAUSA"]], on="COD_CAUSA", how="left")

    # Mes de defunción
    if "MES_DEF" not in df.columns and "FECHA_DEF" in df.columns:
        df["MES_DEF"] = pd.to_datetime(df["FECHA_DEF"]).dt.month
    df["MES_DEF"] = df["MES_DEF"].astype("Int64")

    # Sexo
    if "SEXO" in df.columns:
        df["SEXO"] = df["SEXO"].replace({"M": "Masculino", "F": "Femenino"}).fillna("Sin información")
    else:
        df["SEXO"] = "Sin información"

    # Grupo de edad
    if "GRUPO_EDAD1" in df.columns:
        df["GRUPO_EDAD1"] = df["GRUPO_EDAD1"].astype("Int64")
    else:
        df["GRUPO_EDAD1"] = pd.NA
    df["GRUPO_EDAD_CAT"] = df["GRUPO_EDAD1"].map(age_group_map())

    return df, causas, divipola

def homicide_filter(df):
    # Aproximación de homicidios (ajusta según tu diccionario exacto)
    if "COD_CAUSA" not in df.columns:
        return df.iloc[0:0]
    cod = df["COD_CAUSA"].astype(str)
    mask = cod.str.startswith(("X95", "X96", "X97", "X98", "X99")) | cod.str.startswith(("Y00", "Y01", "Y02", "Y03", "Y04", "Y05", "Y06", "Y07", "Y08", "Y09"))
    return df[mask]

def top_cities_violent(df, top_n=5):
    h = homicide_filter(df)
    grp = h.groupby("MUNICIPIO", dropna=False).size().reset_index(name="HOMICIDIOS")
    return grp.sort_values("HOMICIDIOS", ascending=False).head(top_n)

def lowest_mortality_cities(df, top_n=10):
    grp = df.groupby("MUNICIPIO", dropna=False).size().reset_index(name="TOTAL")
    return grp.sort_values("TOTAL", ascending=True).head(top_n)

def deaths_by_department(df):
    return df.groupby("DEPARTAMENTO", dropna=False).size().reset_index(name="TOTAL")

def deaths_by_month(df):
    return df.groupby("MES_DEF", dropna=False).size().reset_index(name="TOTAL").sort_values("MES_DEF")

def top_causes(df, top_n=10):
    cols = ["COD_CAUSA", "DESC_CAUSA"] if "DESC_CAUSA" in df.columns else ["COD_CAUSA"]
    grp = df.groupby(cols, dropna=False).size().reset_index(name="TOTAL")
    return grp.sort_values("TOTAL", ascending=False).head(top_n)

def deaths_by_sex_department(df):
    return df.groupby(["DEPARTAMENTO", "SEXO"], dropna=False).size().reset_index(name="TOTAL")

def histogram_age(df):
    grp = df.groupby("GRUPO_EDAD_CAT").size().reset_index(name="TOTAL")
    order = [
        "Mortalidad neonatal", "Mortalidad infantil", "Primera infancia", "Niñez",
        "Adolescencia", "Juventud", "Adultez temprana", "Adultez intermedia",
        "Vejez", "Longevidad / Centenarios", "Edad desconocida"
    ]
    grp["ORD"] = grp["GRUPO_EDAD_CAT"].apply(lambda x: order.index(x) if x in order else len(order))
    return grp.sort_values("ORD")

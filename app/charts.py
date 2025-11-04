import plotly.express as px
import plotly.graph_objects as go

def map_departments(df_depto):
    # Choropleth por departamento. Si tienes geojson de departamentos, cámbialo aquí.
    # Como alternativa sin geojson: usar un barmap con treemap. Aquí usamos choropleth nominal con featureidkey si lo incluyes.
    fig = px.choropleth(
        df_depto,
        locations="DEPARTAMENTO",
        locationmode="country names",  # reemplazar por 'geojson-id' si usas geojson
        color="TOTAL",
        color_continuous_scale="Reds",
        labels={"TOTAL": "Muertes"},
        title="Distribución de muertes por departamento (2019)"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    return fig

def line_months(df_month):
    fig = px.line(
        df_month,
        x="MES_DEF", y="TOTAL",
        markers=True,
        labels={"MES_DEF": "Mes", "TOTAL": "Muertes"},
        title="Muertes por mes (2019)"
    )
    fig.update_xaxes(dtick=1)
    return fig

def bar_top_violent(df_violent):
    fig = px.bar(
        df_violent,
        x="MUNICIPIO", y="HOMICIDIOS",
        labels={"MUNICIPIO": "Ciudad", "HOMICIDIOS": "Homicidios"},
        title="Top 5 ciudades más violentas (Homicidios X95)"
    )
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

def pie_lowest_cities(df_lowest):
    fig = px.pie(
        df_lowest,
        names="MUNICIPIO",
        values="TOTAL",
        title="10 ciudades con menor mortalidad (2019)",
        hole=0.25
    )
    return fig

def table_top_causes(df_causes):
    header = dict(values=["Código", "Causa", "Total"], fill_color="#f0f0f0", align="left")
    cells = dict(values=[df_causes["COD_CAUSA"], df_causes["DESC_CAUSA"], df_causes["TOTAL"]], align="left")
    fig = go.Figure(data=[go.Table(header=header, cells=cells)])
    fig.update_layout(title="10 principales causas de muerte (2019)")
    return fig

def stacked_bar_sex_by_department(df_sex_depto):
    fig = px.bar(
        df_sex_depto,
        x="DEPARTAMENTO", y="TOTAL",
        color="SEXO", barmode="stack",
        labels={"DEPARTAMENTO": "Departamento", "TOTAL": "Muertes"},
        title="Muertes por sexo en cada departamento (2019)"
    )
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

def histogram_by_age_group(df_age):
    fig = px.bar(
        df_age,
        x="GRUPO_EDAD_CAT", y="TOTAL",
        labels={"GRUPO_EDAD_CAT": "Grupo de edad", "TOTAL": "Muertes"},
        title="Distribución de muertes por grupo de edad (GRUPO_EDAD1)"
    )
    fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':df_age["GRUPO_EDAD_CAT"].tolist()})
    return fig
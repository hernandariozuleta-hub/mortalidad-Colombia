import dash
from dash import Dash, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd

from data_loader import load_data, deaths_by_department, deaths_by_month, top_cities_violent, lowest_mortality_cities, top_causes, deaths_by_sex_department, histogram_age
from charts import map_departments, line_months, bar_top_violent, pie_lowest_cities, table_top_causes, stacked_bar_sex_by_department, histogram_by_age_group
from layout import build_layout

df, causas, divipola = load_data()

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Mortalidad Colombia 2019"
app.layout = build_layout()

# Poblar opciones dinámicas de departamento
@app.callback(Output("department-filter", "options"), Input("department-filter", "id"))
def fill_departments(_):
    opts = [{"label": d, "value": d} for d in sorted(df["DEPARTAMENTO"].dropna().unique())]
    return opts

def apply_filters(df_in, department=None, sex=None, month=None):
    d = df_in.copy()
    if department:
        d = d[d["DEPARTAMENTO"] == department]
    if sex:
        d = d[d["SEXO"] == sex]
    if month:
        d = d[d["MES_DEF"] == month]
    return d

@app.callback(
    Output("map-departments", "figure"),
    Input("department-filter", "value"),
    Input("sex-filter", "value"),
    Input("month-filter", "value")
)
def update_map(department, sex, month):
    d = apply_filters(df, department, sex, month)
    fig = map_departments(deaths_by_department(d))
    return fig

@app.callback(
    Output("line-months", "figure"),
    Input("department-filter", "value"),
    Input("sex-filter", "value")
)
def update_line(department, sex):
    d = apply_filters(df, department, sex, None)
    fig = line_months(deaths_by_month(d))
    return fig

@app.callback(
    Output("bar-top-violent", "figure"),
    Input("department-filter", "value"),
    Input("month-filter", "value")
)
def update_violent(department, month):
    d = apply_filters(df, department, None, month)
    fig = bar_top_violent(top_cities_violent(d, top_n=5))
    return fig

@app.callback(
    Output("pie-lowest-cities", "figure"),
    Input("department-filter", "value"),
    Input("month-filter", "value")
)
def update_lowest(department, month):
    d = apply_filters(df, department, None, month)
    fig = pie_lowest_cities(lowest_mortality_cities(d, top_n=10))
    return fig

@app.callback(
    Output("table-top-causes", "figure"),
    Input("department-filter", "value"),
    Input("sex-filter", "value"),
    Input("month-filter", "value")
)
def update_table(department, sex, month):
    d = apply_filters(df, department, sex, month)
    fig = table_top_causes(top_causes(d, top_n=10))
    return fig

@app.callback(
    Output("stacked-bar-sex-dept", "figure"),
    Input("month-filter", "value")
)
def update_stacked(month):
    d = apply_filters(df, None, None, month)
    fig = stacked_bar_sex_by_department(deaths_by_sex_department(d))
    return fig

@app.callback(
    Output("histogram-age-group", "figure"),
    Input("department-filter", "value"),
    Input("sex-filter", "value")
)
def update_histogram(department, sex):
    d = apply_filters(df, department, sex, None)
    fig = histogram_by_age_group(histogram_age(d))
    return fig

server = app.server

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
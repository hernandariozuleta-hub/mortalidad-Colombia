from dash import html, dcc
import dash_bootstrap_components as dbc

def build_layout():
    return dbc.Container(fluid=True, children=[
        html.H2("Mortalidad en Colombia - 2019"),
        html.P("Exploración interactiva de mortalidad por departamento, mes, causa, sexo y grupo de edad."),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="department-filter",
                placeholder="Filtrar por departamento (opcional)",
                multi=False
            ), md=4),
            dbc.Col(dcc.Dropdown(
                id="sex-filter",
                options=[{"label":"Masculino", "value":"Masculino"},
                         {"label":"Femenino", "value":"Femenino"},
                         {"label":"Sin información", "value":"Sin información"}],
                placeholder="Filtrar por sexo (opcional)",
                multi=False
            ), md=4),
            dbc.Col(dcc.Dropdown(
                id="month-filter",
                options=[{"label":str(m), "value":m} for m in range(1,13)],
                placeholder="Filtrar por mes (opcional)",
                multi=False
            ), md=4),
        ], className="mb-3"),
        dbc.Row([
            dbc.Col(dcc.Graph(id="map-departments"), md=6),
            dbc.Col(dcc.Graph(id="line-months"), md=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="bar-top-violent"), md=6),
            dbc.Col(dcc.Graph(id="pie-lowest-cities"), md=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="table-top-causes"), md=6),
            dbc.Col(dcc.Graph(id="stacked-bar-sex-dept"), md=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="histogram-age-group"), md=12),
        ]),
        html.Hr(),
        html.Small("Fuente: Microdatos de mortalidad no fetal 2019. Diccionario de causas y DIVIPOLA."),
    ])

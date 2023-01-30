import dash
from dash import Dash, html
import dash_bootstrap_components as dbc



app = Dash(__name__,use_pages=True,
external_stylesheets=[dbc.themes.CYBORG])
app.config.suppress_callback_exceptions = True
server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Home", href="/pages/home",header=True),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Geographical analysis", href="/pages/geo"),
                dbc.DropdownMenuItem("Candidate analysis", href="/pages/candidate"),
            ],
            nav=True,
            in_navbar=True,
            label="Menu",
        ),
    ],
    brand="French 2022 presidential elections first round results analysis",
    brand_href="/",
    color="primary",
    dark=True,
)

app.layout = html.Div([navbar,

	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True,host="0.0.0.0",port=8080)

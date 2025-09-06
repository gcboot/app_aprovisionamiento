from dash import Dash, html
from db import supabase_client

app  = Dash(__name__)

app.layout =([
    html.Div("Plataforma de Aprovisionamiento"),
    html.P("Bienvenido a la app en Dash conectada con Supabase.")   
])

if __name__ == '__main__':
    app.run_server(debug=True)

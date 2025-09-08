import dash
from dash import html
from src.components.layout_base import layout_base

dash.register_page(__name__, path="/home", title="Panel Principal")

layout = layout_base(
    html.Div([
        html.H2(id="welcome-message"),   # 👈 IMPORTANTE: este id debe existir
        html.P("Aquí verás el resumen de la plataforma.")
    ])
)

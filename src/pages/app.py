# src/pages/app.py
import dash_mantine_components as dmc
from dash import html

def main_layout():
    return html.Div(
        style={"padding": "40px"},
        children=[
            dmc.Title("Dashboard Principal", order=1),
            dmc.Space(h=20),
            dmc.Button("Cerrar Sesión", id="btn-logout", color="red"),
            dmc.Text(id="logout-message", c="gray")
        ]
    )

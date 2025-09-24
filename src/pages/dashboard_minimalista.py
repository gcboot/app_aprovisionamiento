import dash
from dash import html, dcc
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd

from src.components.layout_base import layout_base

# Registrar página
dash.register_page(
    __name__,
    path="/home/dashboard_minimalista",
    name="Dashboard Minimalista"
)

def layout():
    # Placeholder gráfico comparativo
    df = pd.DataFrame({
        "Campaña": ["C10", "C11", "C12", "C13"],
        "Proyección": [1000, 1500, 1200, 2000],
        "Ventas Reales": [900, 1400, 1100, 2200]
    })
    df_melted = df.melt(id_vars="Campaña", var_name="Variable", value_name="Valor")
    fig_bar = px.bar(df_melted, x="Campaña", y="Valor", color="Variable", barmode="group",
                     title="Proyección vs Ventas Reales")

    # Placeholder gráfico secundario
    fig_pie = px.pie(
        values=[45, 25, 20, 10],
        names=["Belleza", "Hogar", "Vitaminas", "Perfumería"],
        title="Distribución de Ventas"
    )

    # Tabla resumen placeholder
    tabla = dmc.Table(
        [
            html.Thead(html.Tr([
                html.Th("Campaña"),
                html.Th("País"),
                html.Th("Unidades"),
                html.Th("Desviación %")
            ])),
            html.Tbody([
                html.Tr([html.Td("C08-2025"), html.Td("GT"), html.Td("1200"), html.Td("-12%")]),
                html.Tr([html.Td("C09-2025"), html.Td("HN"), html.Td("980"), html.Td("-15%")]),
                html.Tr([html.Td("C10-2025"), html.Td("SV"), html.Td("1500"), html.Td("0%")]),
            ])
        ],
        striped=True,
        highlightOnHover=True,
        withTableBorder=True
    )

    contenido = dmc.Container([

        dmc.Title("📊 Panel de Control – Minimalista", order=2, mb=20),

        dmc.Grid([
            dmc.GridCol(dcc.Graph(figure=fig_bar), span=6),
            dmc.GridCol(dcc.Graph(figure=fig_pie), span=6),
        ], mb=30),

        tabla
    ], fluid=True)

    return layout_base(contenido)

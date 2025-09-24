import dash
from dash import html, dcc
import dash_mantine_components as dmc
import plotly.express as px

from src.components.layout_base import layout_base

# Registrar página
dash.register_page(
    __name__,
    path="/home/dashboard_alertas",
    name="Dashboard Alertas Predictivas"
)

def layout():
    # Placeholder gráfica lateral
    fig_pie = px.pie(
        values=[40, 30, 20, 10],
        names=["GT", "HN", "SV", "NI"],
        title="Distribución de Ventas"
    )

    contenido = dmc.Container([

        dmc.Title("📊 Panel de Control – Alertas Predictivas", order=2, mb=20),

        # KPIs mínimos
        dmc.Group([
            dmc.Paper(dmc.Stack([
                dmc.Text("Campañas Analizadas", size="sm", fw=500),
                dmc.Text("12", size="xl", fw=700, c="blue")
            ]), shadow="sm", p="md", radius="md"),

            dmc.Paper(dmc.Stack([
                dmc.Text("Precisión del Modelo", size="sm", fw=500),
                dmc.Text("92%", size="xl", fw=700, c="green")
            ]), shadow="sm", p="md", radius="md"),

            dmc.Paper(dmc.Stack([
                dmc.Text("Alertas Activas", size="sm", fw=500),
                dmc.Text("3", size="xl", fw=700, c="orange")
            ]), shadow="sm", p="md", radius="md"),
        ], mb=30, grow=True),

        # Bloques de alertas
        dmc.Stack([
            dmc.Alert("⚠️ C08-2025 – Riesgo de quiebre en 2 productos", color="red", variant="light"),
            dmc.Alert("📉 C09-2025 – Ventas -15% vs proyección", color="yellow", variant="light"),
            dmc.Alert("✅ C10-2025 – Desempeño estable", color="green", variant="light"),
        ], mb=30),

        # Gráfica lateral
        dcc.Graph(figure=fig_pie)
    ], fluid=True)

    return layout_base(contenido)

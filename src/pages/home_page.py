import dash
from dash import html, dcc
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd

from src.components.layout_base import layout_base

dash.register_page(__name__, path="/home", title="Panel Principal")

# ---------- Datos de ejemplo (reemplazar luego con supabase) ----------
df_proyecciones = pd.DataFrame({
    "Campaña": ["C10", "C11", "C12", "C13"],
    "Proyección": [1000, 1500, 1200, 2000],
    "Ventas Reales": [900, 1400, 1100, 2200],
})

df_inventario = pd.DataFrame({
    "Categoría": ["Belleza", "Hogar", "Vitaminas", "Perfumería"],
    "Unidades": [5000, 3000, 2000, 1500],
})

fig_proy = px.bar(
    df_proyecciones,
    x="Campaña",
    y=["Proyección", "Ventas Reales"],
    barmode="group",
    title="Proyección vs Ventas Reales",
)

fig_inv = px.pie(
    df_inventario,
    names="Categoría",
    values="Unidades",
    title="Distribución de Inventario",
)

# ---------- Layout ----------
layout = layout_base(
    dmc.Container(
        [
            # Bienvenida dinámica (se llena con tu callback)
            html.H1(id="welcome-message"),

            # Encabezado del dashboard
            dmc.Stack(
                [
                    dmc.Title(
                        "Panel de Control – Plataforma de Análisis Predictivo",
                        order=2,
                        c="blue",
                        mb=5,
                    ),
                    dmc.Text(
                        "Visión general de las operaciones, inventario y proyecciones de campañas.",
                        c="dimmed",
                        size="sm",
                        mb=30,
                    ),
                ],
                gap="xs",  # 👈 corregido (antes era spacing)
            ),

            # ---------- KPIs ----------
            dmc.Grid(
                [
                    dmc.GridCol(
                        dmc.Paper(
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            p="md",
                            children=[
                                dmc.Text("Productos Activos", size="sm", c="dimmed"),
                                dmc.Title("120", order=3, c="blue"),
                            ],
                        ),
                        span=3,
                    ),
                    dmc.GridCol(
                        dmc.Paper(
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            p="md",
                            children=[
                                dmc.Text("Inventario Disponible", size="sm", c="dimmed"),
                                dmc.Title("11,500", order=3, c="green"),
                            ],
                        ),
                        span=3,
                    ),
                    dmc.GridCol(
                        dmc.Paper(
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            p="md",
                            children=[
                                dmc.Text("Proyecciones Generadas", size="sm", c="dimmed"),
                                dmc.Title("8", order=3, c="orange"),
                            ],
                        ),
                        span=3,
                    ),
                    dmc.GridCol(
                        dmc.Paper(
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            p="md",
                            children=[
                                dmc.Text("Alertas de Quiebre", size="sm", c="dimmed"),
                                dmc.Title("3", order=3, c="red"),
                            ],
                        ),
                        span=3,
                    ),
                ],
                gutter="lg",
                mb=40,
            ),

            # ---------- Gráficas ----------
            dmc.Grid(
                [
                    dmc.GridCol(
                        dcc.Graph(figure=fig_proy, style={"height": "400px"}),
                        span=6,
                    ),
                    dmc.GridCol(
                        dcc.Graph(figure=fig_inv, style={"height": "400px"}),
                        span=6,
                    ),
                ],
                gutter="lg",
            ),
        ],
        fluid=True,
    )
)

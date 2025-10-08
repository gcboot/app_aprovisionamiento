import dash
from dash import html, dcc
import dash_mantine_components as dmc
from src.components.layout_base import layout_base

# Registrar página
dash.register_page(
    __name__,
    path="/home/ventas",
    name="Ventas"
)


def layout():
    content = dmc.Container([

        dmc.Title("Ventas", order=2, mb=30),

        # ---------- Card: Carga y procesamiento ----------
        dmc.Card(
            withBorder=True, shadow="sm", radius="md", mb=30,
            children=[
                dmc.Title("Carga de ventas (staging)", order=3, mb=15),

                dcc.Upload(
                    id="upload-ventas",
                    children=dmc.Button("📂 Cargar CSV de Ventas", color="blue"),
                    multiple=False
                ),
                html.Div(id="preview-staging", style={"marginTop": "15px"}),

                dmc.Button(
                    "⚡ Procesar staging",
                    id="btn-procesar-staging",
                    color="green",
                    mt=20
                ),
                html.Div(id="resultado-etl", style={"marginTop": "10px"})
            ]
        ),

        # ---------- Card: Ventas procesadas ----------
        dmc.Card(
            withBorder=True, shadow="sm", radius="md", mb=30,
            children=[
                dmc.Title("Ventas procesadas", order=3, mb=15),

                dmc.SimpleGrid(
                    cols=4,
                    spacing="lg",
                    children=[
                        dmc.Select(
                            label="Campaña",
                            placeholder="Selecciona campaña",
                            id="filtro-campania",
                            data=[], clearable=True
                        ),
                        dmc.Select(
                            label="País",
                            placeholder="Selecciona país",
                            id="filtro-pais",
                            data=[], clearable=True
                        ),
                        dmc.TextInput(
                            label="Producto",
                            placeholder="Código o nombre",
                            id="filtro-producto"
                        ),
                        dmc.DatePickerInput(
                            label="Rango de Fechas",
                            type="range",
                            id="filtro-fechas"
                        ),
                    ]
                ),

                dmc.Button("🔍 Filtrar", id="btn-filtrar-ventas", color="blue", mt=20),
                html.Div(id="tabla-ventas")
            ]
        ),

        # ---------- Card: Eventos ----------
        dmc.Card(
            withBorder=True, shadow="sm", radius="md",
            children=[
                dmc.Title("Eventos de venta", order=3, mb=15),

                dmc.SimpleGrid(
                    cols=3,
                    spacing="lg",
                    children=[
                        dmc.Select(
                            label="Tipo Evento",
                            placeholder="Selecciona tipo",
                            id="filtro-tipo-evento",
                            data=[
                                {"value": "agotado_web", "label": "Agotado Web"},
                                {"value": "pedido_bloqueado", "label": "Pedido Bloqueado"}
                            ],
                            clearable=True
                        ),
                        dmc.Select(
                            label="Campaña",
                            placeholder="Selecciona campaña",
                            id="filtro-campania-evento",
                            data=[], clearable=True
                        ),
                        dmc.TextInput(
                            label="Producto",
                            placeholder="Código o nombre",
                            id="filtro-producto-evento"
                        ),
                    ]
                ),

                dmc.Button("🔍 Filtrar eventos", id="btn-filtrar-eventos", color="blue", mt=20),
                html.Div(id="tabla-eventos")
            ]
        )
    ], fluid=True)

    return layout_base(content)

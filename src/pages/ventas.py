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

        # ---------- Título ----------
        dmc.Title("Ventas", order=2, mb=20),

        # ---------- Carga CSV ----------
        dcc.Upload(
            id="upload-ventas",
            children=dmc.Button("📂 Cargar CSV de Ventas", color="blue"),
            multiple=False
        ),
        html.Div(id="preview-staging", style={"marginTop": "10px"}),

        # ---------- Procesar staging ----------
        dmc.Button(
            "⚡ Procesar staging",
            id="btn-procesar-staging",
            color="green",
            mt=20
        ),
        html.Div(id="resultado-etl", style={"marginTop": "10px"}),

        # ---------- Ventas ----------
        dmc.Divider(label="Ventas procesadas", mt=30, mb=10),

        # Filtros ventas
        dmc.Group([
            dmc.Select(
                label="Campaña",
                placeholder="Selecciona campaña",
                id="filtro-campania",
                data=[],          # Se llena desde callback
                clearable=True
            ),
            dmc.Select(
                label="País",
                placeholder="Selecciona país",
                id="filtro-pais",
                data=[],          # Se llena desde callback
                clearable=True
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
            dmc.Button("🔍 Filtrar", id="btn-filtrar-ventas", color="blue", mt=22)
        ], grow=True, mb=20),

        dmc.Paper(
            shadow="sm", p="md", withBorder=True, radius="md",
            children=html.Div(id="tabla-ventas")
        ),

        # ---------- Eventos ----------
        dmc.Divider(label="Eventos de venta", mt=30, mb=10),

        # Filtros eventos
        dmc.Group([
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
                data=[],          # Se llena desde callback
                clearable=True
            ),
            dmc.TextInput(
                label="Producto",
                placeholder="Código o nombre",
                id="filtro-producto-evento"
            ),
            dmc.Button("🔍 Filtrar eventos", id="btn-filtrar-eventos", color="blue", mt=22)
        ], grow=True, mb=20),

        dmc.Paper(
            shadow="sm", p="md", withBorder=True, radius="md",
            children=html.Div(id="tabla-eventos")
        ),
    ], fluid=True)

    # 👇 Envolvemos todo con tu layout base
    return layout_base(content)

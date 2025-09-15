import dash
from dash import html, dcc
import dash_mantine_components as dmc
from src.components.layout_base import layout_base

dash.register_page(__name__, path="/home/categorias", name="Categorías")

layout = layout_base(
    dmc.Stack([

        # Botón para crear categoría
        dmc.Button(
            "➕ Nueva Categoría",
            id="btn-add-categoria",
            color="teal",
            variant="filled",
            radius="md",
            size="sm",
            style={"width": "200px", "marginBottom": "10px"}
        ),

        # Mensajes (éxito / error)
        html.Div(id="notificacion-categoria"),

        # Tabla de categorías
        html.Div(id="tabla-categorias"),

        # Modal CRUD Categorías
        dmc.Modal(
            id="modal-categoria",
            opened=False,
            title="Categoría",
            centered=True,
            size="lg",
            overlayProps={
                "opacity": 0.55,
                "blur": 3
            },
            children=[
                dmc.TextInput(
                    id="input-nombre-categoria",
                    label="Nombre",
                    required=True,
                    radius="md",
                    mb=10
                ),
                dmc.Textarea(
                    id="input-descripcion-categoria",
                    label="Descripción",
                    radius="md",
                    autosize=True,
                    minRows=3,
                    mb=20
                ),
                dmc.Button(
                    "Guardar",
                    id="btn-save-categoria",
                    fullWidth=True,
                    color="blue",
                    radius="md",
                    size="md"
                )
            ]
        ),

        # Stores auxiliares
        dcc.Store(id="categoria-edit-id", storage_type="memory"),
        dcc.Store(id="trigger-refresh-categorias", storage_type="memory")  # 👈 necesario para refrescar tabla
    ]),
    titulo="Mantenimiento de Categorías"
)

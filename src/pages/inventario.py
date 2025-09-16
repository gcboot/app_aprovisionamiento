import dash
from dash import html, dcc
import dash_mantine_components as dmc
from src.components.layout_base import layout_base

dash.register_page(__name__, path="/home/inventario", name="Inventario")

layout = layout_base(
    dmc.Stack([

        # Botón para crear registro
        dmc.Button(
            "➕ Nuevo Registro",
            id="inventario_btn_add",
            color="teal",
            variant="filled",
            radius="md",
            size="sm",
            style={"width": "200px", "marginBottom": "10px"}
        ),

        # Mensajes
        html.Div(id="inventario_notificacion"),

        # Tabla
        html.Div(id="inventario_tabla"),

        # Modal CRUD
        dmc.Modal(
            id="inventario_modal",
            opened=False,
            title="Inventario",
            centered=True,
            size="lg",
            overlayProps={"opacity": 0.55, "blur": 3},
            children=[

                # Solo productos originales
                dmc.Select(
                    id="inventario_input_producto",
                    label="Producto (solo originales)",
                    data=[],  # se carga dinámicamente
                    required=True,
                    radius="md",
                    mb=10
                ),

                dmc.NumberInput(id="inventario_input_stock_inicial", label="Stock Inicial", min=0, step=1, radius="md", mb=10),
                dmc.NumberInput(id="inventario_input_stock_actual", label="Stock Actual", min=0, step=1, radius="md", mb=10),
                dmc.NumberInput(id="inventario_input_stock_minimo", label="Stock Mínimo", min=0, step=1, radius="md", mb=10),
                dmc.NumberInput(id="inventario_input_stock_reservado", label="Stock Reservado", min=0, step=1, radius="md", mb=10),

                # Fecha (simulamos etiqueta con Text)
                dmc.Stack([
                    dmc.Text("Fecha", size="sm", fw=500),
                    dmc.DatePicker(
                        id="inventario_input_fecha",
                        mb=20,
                        style={"width": "100%"}  # ocupa todo el ancho
                    )
                ]),

                dmc.Button(
                    "Guardar",
                    id="inventario_btn_save",
                    fullWidth=True,
                    color="blue",
                    radius="md",
                    size="md"
                )
            ]
        ),

        # Stores auxiliares
        dcc.Store(id="inventario_edit_id", storage_type="memory"),
        dcc.Store(id="inventario_trigger_refresh", storage_type="memory")
    ]),
    titulo="Mantenimiento de Inventario"
)

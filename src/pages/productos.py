import dash
from dash import html, dcc
import dash_mantine_components as dmc
from src.components.layout_base import layout_base

dash.register_page(__name__, path="/home/productos", name="Productos")

layout = layout_base(
    dmc.Stack([

        # Botón para crear producto
        dmc.Button(
            "➕ Nuevo Producto",
            id="productos_btn_add",
            color="teal",
            variant="filled",
            radius="md",
            size="sm",
            style={"width": "200px", "marginBottom": "10px"}
        ),

        # Mensajes (éxito / error)
        html.Div(id="productos_notificacion"),

        # Tabla de productos
        html.Div(id="productos_tabla"),

        # Modal CRUD Productos
        dmc.Modal(
            id="productos_modal",
            opened=False,
            title="Producto",
            centered=True,
            size="lg",
            overlayProps={"opacity": 0.55, "blur": 3},
            children=[

                dmc.NumberInput(
                    id="productos_input_codigo",
                    label="Código",
                    step=1,
                    required=True,
                    radius="md",
                    mb=10
                ),

                dmc.TextInput(
                    id="productos_input_nombre",
                    label="Nombre",
                    required=True,
                    radius="md",
                    mb=10
                ),

                dmc.NumberInput(
                    id="productos_input_precio",
                    label="Precio Base (Q)",
                    step=0.01,
                    decimalScale=2,      # ✅ permitido en tu versión
                    fixedDecimalScale=True,
                    radius="md",
                    mb=10
                ),

                dmc.Select(
                    id="productos_input_es_original",
                    label="Tipo de producto",
                    data=[
                        {"label": "Original", "value": "true"},
                        {"label": "Ofertado", "value": "false"},
                    ],
                    radius="md",
                    mb=10
                ),

                # Contenedor oculto: solo aparece si es ofertado
                html.Div(
                    dmc.Select(
                        id="productos_input_original",
                        label="Producto Original",
                        data=[],  # 👈 se carga dinámicamente en el callback
                        radius="md",
                        mb=20
                    ),
                    id="productos_original_container",
                    style={"display": "none"}
                ),

                # ⚠️ IMPORTANTE: en esta primera versión lo dejamos como NumberInput,
                # pero lo ideal sería convertirlo en un Select dinámico más adelante.
                dmc.NumberInput(
                    id="productos_input_categoria",
                    label="ID Categoría",
                    step=1,
                    required=False,
                    radius="md",
                    mb=20
                ),

                dmc.Button(
                    "Guardar",
                    id="productos_btn_save",
                    fullWidth=True,
                    color="blue",
                    radius="md",
                    size="md"
                )
            ]
        ),

        # Stores auxiliares
        dcc.Store(id="productos_edit_id", storage_type="memory"),
        dcc.Store(id="productos_trigger_refresh", storage_type="memory")
    ]),
    titulo="Mantenimiento de Productos"
)

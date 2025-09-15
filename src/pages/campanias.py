import dash
from dash import html, dcc
import dash_mantine_components as dmc
from src.components.layout_base import layout_base

dash.register_page(__name__, path="/home/campanias", name="Campañas")

layout = layout_base(
    dmc.Stack([

        # Botón para crear campaña
        dmc.Button(
            "➕ Nueva Campaña",
            id="campanias_btn_add",
            color="teal",
            variant="filled",
            radius="md",
            size="sm",
            style={"width": "200px", "marginBottom": "10px"}
        ),

        # Mensajes (éxito / error)
        html.Div(id="campanias_notificacion"),

        # Tabla de campañas
        html.Div(id="campanias_tabla"),

        # Modal CRUD Campañas
        dmc.Modal(
            id="campanias_modal",
            opened=False,
            title="Campaña",
            centered=True,
            size="lg",
            overlayProps={
                "opacity": 0.55,
                "blur": 3
            },
            children=[
                dmc.TextInput(
                    id="campanias_input_nombre",
                    label="Nombre de la campaña",
                    required=True,
                    radius="md",
                    mb=10
                ),
                dmc.NumberInput(
                    id="campanias_input_anio",
                    label="Año",
                    required=True,
                    radius="md",
                    mb=10
                ),
                # Fecha inicio (sin props no soportadas)
                dmc.Stack([
                    dmc.Text("Fecha inicio", size="sm"),
                    dmc.DatePicker(
                        id="campanias_input_fecha_inicio",
                        mb=10,
                        style={"width": "100%"}
                    ),
                ]),
                # Fecha fin (sin props no soportadas)
                dmc.Stack([
                    dmc.Text("Fecha fin", size="sm"),
                    dmc.DatePicker(
                        id="campanias_input_fecha_fin",
                        mb=10,
                        style={"width": "100%"}
                    ),
                ]),
                dmc.Select(
                    id="campanias_input_estado",
                    label="Estado",
                    data=[
                        {"label": "Programada", "value": "programada"},
                        {"label": "Activa", "value": "activa"},
                        {"label": "Finalizada", "value": "finalizada"},
                    ],
                    radius="md",
                    mb=20
                ),
                dmc.Button(
                    "Guardar",
                    id="campanias_btn_save",
                    fullWidth=True,
                    color="blue",
                    radius="md",
                    size="md"
                )
            ]
        ),

        # Stores auxiliares
        dcc.Store(id="campanias_edit_id", storage_type="memory"),
        dcc.Store(id="campanias_trigger_refresh", storage_type="memory")  # 👈 necesario para refrescar tabla
    ]),
    titulo="Mantenimiento de Campañas"
)

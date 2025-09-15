from dash import Input, Output, State, ALL, ctx, no_update, html
import dash_mantine_components as dmc
from src.models import campanias
from datetime import datetime

def format_date(date_str):
    if not date_str:
        return ""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return date_str  # fallback si ya viene en otro formato


def register_campanias_callbacks(app):

    # ---------- Renderizar tabla ----------
    def render_tabla_campanias():
        camps = campanias.get_campanias()
        if not camps:
            return dmc.Alert(
                "No hay campañas registradas.",
                color="yellow",
                variant="filled",
                radius="md",
                mt=10,
            )

        rows = [
            html.Tr([
                html.Td(camp["campania"]),
                html.Td(camp["anio"]),
                html.Td(format_date(camp.get("fecha_inicio"))),
                html.Td(format_date(camp.get("fecha_fin"))),
                html.Td(camp.get("estado", "")),
                html.Td(
                    dmc.Group(
                        [
                            dmc.Button(
                                "Editar",
                                color="blue",
                                size="xs",
                                variant="light",
                                id={"type": "btn-edit-campania", "index": camp["id"]},
                            ),
                            dmc.Button(
                                "Eliminar",
                                color="red",
                                size="xs",
                                variant="outline",
                                id={"type": "btn-del-campania", "index": camp["id"]},
                            ),
                        ],
                        gap="sm",
                        justify="flex-end",
                    ),
                    style={"textAlign": "right"},
                ),
            ])
            for camp in camps
        ]

        return dmc.Table(
            children=[
                html.Thead(
                    html.Tr(
                        [
                            html.Th("Campaña"),
                            html.Th("Año"),
                            html.Th("Fecha inicio"),
                            html.Th("Fecha fin"),
                            html.Th("Estado"),
                            html.Th("Acciones", style={"textAlign": "right"}),
                        ]
                    ),
                    style={"backgroundColor": "#f5f6fa"},
                ),
                html.Tbody(rows),
            ],
            striped=True,
            highlightOnHover=True,
            withTableBorder=True,
            withRowBorders=True,
            withColumnBorders=True,
            horizontalSpacing="md",
            verticalSpacing="sm",
            mt=10,
            mb=20,
            style={"borderRadius": "8px", "overflow": "hidden", "textAlign": "center"},
        )

    # ---------- Actualizar tabla ----------
    @app.callback(
        Output("campanias_tabla", "children"),
        Input("campanias_btn_add", "n_clicks"),
        Input("campanias_trigger_refresh", "data"),
        Input({"type": "btn-del-campania", "index": ALL}, "n_clicks"),
        prevent_initial_call=False,
    )
    def actualizar_tabla_campanias(_, refresh_trigger, __):
        triggered = ctx.triggered_id
        if isinstance(triggered, dict) and "index" in triggered:  # eliminar
            campanias.delete_campania(triggered["index"])
        return render_tabla_campanias()

    # ---------- Manejar modal (crear / editar / guardar) ----------
    @app.callback(
        Output("campanias_modal", "opened"),
        Output("campanias_input_nombre", "value"),
        Output("campanias_input_anio", "value"),
        Output("campanias_input_fecha_inicio", "value"),
        Output("campanias_input_fecha_fin", "value"),
        Output("campanias_input_estado", "value"),
        Output("campanias_edit_id", "data"),
        Output("campanias_notificacion", "children"),
        Output("campanias_trigger_refresh", "data"),
        Input("campanias_btn_add", "n_clicks"),
        Input({"type": "btn-edit-campania", "index": ALL}, "n_clicks"),
        Input("campanias_btn_save", "n_clicks"),
        State("campanias_input_nombre", "value"),
        State("campanias_input_anio", "value"),
        State("campanias_input_fecha_inicio", "value"),
        State("campanias_input_fecha_fin", "value"),
        State("campanias_input_estado", "value"),
        State("campanias_edit_id", "data"),
        prevent_initial_call=True,
    )
    def manejar_modal_campanias(n_crear, n_editar, n_guardar,
                                nombre, anio, fecha_inicio, fecha_fin, estado, edit_id):
        triggered = ctx.triggered_id

        # ➕ CREAR → abrir modal vacío
        if triggered == "campanias_btn_add":
            return True, "", "", "", "", "", None, no_update, no_update

        # ✏️ EDITAR → abrir modal con datos existentes
        if isinstance(triggered, dict) and "index" in triggered and n_editar and any(n_editar):
            camp = next((c for c in campanias.get_campanias() if c["id"] == triggered["index"]), None)
            if camp:
                return True, camp["campania"], camp["anio"], camp.get("fecha_inicio", ""), camp.get("fecha_fin", ""), camp.get("estado", ""), camp["id"], no_update, no_update

        # 💾 GUARDAR → insertar o actualizar
        if triggered == "campanias_btn_save":
            if not nombre:
                return (
                    no_update, no_update, no_update, no_update, no_update, no_update, no_update,
                    dmc.Alert(
                        "⚠️ El nombre de campaña es obligatorio",
                        color="red",
                        variant="filled",
                        radius="md",
                        mt=10,
                    ),
                    no_update,
                )

            if edit_id:  # actualizar
                campanias.update_campania(edit_id, nombre, anio, fecha_inicio, fecha_fin, estado)
                mensaje = "✅ Campaña actualizada con éxito"
            else:       # insertar
                campanias.insert_campania(nombre, anio, fecha_inicio, fecha_fin, estado)
                mensaje = "✅ Campaña creada con éxito"

            return (
                False, "", "", "", "", "", None,
                dmc.Alert(mensaje, color="green", variant="filled", radius="md", mt=10),
                True,  # refrescar tabla
            )

        # 🔴 DEFAULT → no cambia nada
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

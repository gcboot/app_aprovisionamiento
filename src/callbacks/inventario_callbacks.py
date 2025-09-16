from dash import Input, Output, State, ALL, ctx, no_update, html
import dash_mantine_components as dmc
from src.models import inventario, productos
from src.core.db import supabase
from datetime import datetime

def register_inventario_callbacks(app):

    # ---------- Renderizar tabla ----------
    def render_tabla_inventario():
        inv = inventario.get_inventario()
        if not inv:
            return dmc.Alert("No hay registros de inventario.", color="yellow", variant="filled", radius="md", mt=10)

        rows = []
        for i in inv:
            # Formatear fecha a dd/mm/yyyy
            fecha_str = ""
            if i.get("fecha"):
                try:
                    fecha_str = datetime.strptime(i["fecha"], "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    fecha_str = i["fecha"]

            rows.append(
                html.Tr([
                    html.Td(i["codigo"], style={"textAlign": "center"}),
                    html.Td(i["stock_inicial"], style={"textAlign": "center"}),
                    html.Td(i["stock_actual"], style={"textAlign": "center"}),
                    html.Td(i["stock_minimo"], style={"textAlign": "center"}),
                    html.Td(i["stock_reservado"], style={"textAlign": "center"}),
                    html.Td(fecha_str, style={"textAlign": "center"}),
                    html.Td(
                        dmc.Group([
                            dmc.Button("Editar", color="blue", size="xs", variant="light",
                                    id={"type": "btn-edit-inventario", "index": i["id"]}),
                            dmc.Button("Eliminar", color="red", size="xs", variant="outline",
                                    id={"type": "btn-del-inventario", "index": i["id"]}),
                        ], gap="sm", justify="flex-end"),
                        style={"textAlign": "center"},
                    ),
                ])
            )

        return dmc.Table(
            children=[
                html.Thead(html.Tr([
                    html.Th("Código"),
                    html.Th("Stock Inicial"),
                    html.Th("Stock Actual"),
                    html.Th("Mínimo"),
                    html.Th("Reservado"),
                    html.Th("Fecha"),
                    html.Th("Acciones", style={"textAlign": "right"}),
                ]), style={"backgroundColor": "#f5f6fa"}),
                html.Tbody(rows),
            ],
            striped=True,
            highlightOnHover=True,
            withTableBorder=True,
            mt=10,
            mb=20,
            style={"borderRadius": "8px", "overflow": "hidden", "textAlign": "center"},
        )

    # ---------- Actualizar tabla ----------
    @app.callback(
        Output("inventario_tabla", "children"),
        Input("inventario_btn_add", "n_clicks"),
        Input("inventario_trigger_refresh", "data"),
        Input({"type": "btn-del-inventario", "index": ALL}, "n_clicks"),
        prevent_initial_call=False,
    )
    def actualizar_tabla_inventario(_, refresh_trigger, __):
        triggered = ctx.triggered_id
        if isinstance(triggered, dict) and "index" in triggered:
            inventario.delete_inventario(triggered["index"])
        return render_tabla_inventario()

    # ---------- Cargar productos originales ----------
    @app.callback(
        Output("inventario_input_producto", "data"),
        Input("inventario_btn_add", "n_clicks"),
        prevent_initial_call=True
    )
    def cargar_productos_originales(_):
        originales = productos.get_productos_originales()
        return [
            {"label": f"{p['codigo']} - {p['nombre']}", "value": str(p["codigo"])}
            for p in originales
        ]

    # ---------- Manejar modal ----------
    @app.callback(
        Output("inventario_modal", "opened"),
        Output("inventario_input_producto", "value"),
        Output("inventario_input_stock_inicial", "value"),
        Output("inventario_input_stock_actual", "value"),
        Output("inventario_input_stock_minimo", "value"),
        Output("inventario_input_stock_reservado", "value"),
        Output("inventario_input_fecha", "value"),
        Output("inventario_edit_id", "data"),
        Output("inventario_notificacion", "children"),
        Output("inventario_trigger_refresh", "data"),
        Input("inventario_btn_add", "n_clicks"),
        Input({"type": "btn-edit-inventario", "index": ALL}, "n_clicks"),
        Input("inventario_btn_save", "n_clicks"),
        State("inventario_input_producto", "value"),
        State("inventario_input_stock_inicial", "value"),
        State("inventario_input_stock_actual", "value"),
        State("inventario_input_stock_minimo", "value"),
        State("inventario_input_stock_reservado", "value"),
        State("inventario_input_fecha", "value"),
        State("inventario_edit_id", "data"),
        prevent_initial_call=True,
    )
    def manejar_modal_inventario(n_crear, n_editar, n_guardar,
                                 codigo, stock_inicial, stock_actual, stock_minimo, stock_reservado, fecha, edit_id):
        triggered = ctx.triggered_id

        # ➕ CREAR
        if triggered == "inventario_btn_add":
            return True, None, 0, 0, 0, 0, None, None, no_update, no_update

        # ✏️ EDITAR
        if isinstance(triggered, dict) and "index" in triggered and n_editar and any(n_editar):
            inv = next((i for i in inventario.get_inventario() if i["id"] == triggered["index"]), None)
            if inv:
                # fecha en formato ISO para el DatePicker
                fecha_iso = None
                if inv.get("fecha"):
                    try:
                        fecha_iso = datetime.strptime(inv["fecha"], "%Y-%m-%d").strftime("%Y-%m-%d")
                    except:
                        fecha_iso = inv["fecha"]

                return (
                    True,
                    inv["codigo"],
                    inv["stock_inicial"],
                    inv["stock_actual"],
                    inv["stock_minimo"],
                    inv["stock_reservado"],
                    fecha_iso,
                    inv["id"],
                    no_update,
                    no_update,
                )

        # 💾 GUARDAR
        if triggered == "inventario_btn_save":
            if not codigo:
                return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                       dmc.Alert("⚠️ Debe seleccionar un producto original", color="red", variant="filled", radius="md", mt=10), no_update

            if edit_id:
                inventario.update_inventario(edit_id, stock_inicial, stock_actual, stock_minimo, stock_reservado, fecha)
                mensaje = "✅ Inventario actualizado con éxito"
            else:
                inventario.insert_inventario(codigo, stock_inicial, stock_actual, stock_minimo, stock_reservado, fecha)
                mensaje = "✅ Inventario creado con éxito"

            return False, None, 0, 0, 0, 0, None, None, \
                   dmc.Alert(mensaje, color="green", variant="filled", radius="md", mt=10), True

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

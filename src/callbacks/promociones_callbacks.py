from dash import Input, Output, State, ALL, ctx, no_update, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from src.models import promociones
from datetime import datetime


def register_promociones_callbacks(app):

    # ---------- Renderizar tabla ----------
    def render_tabla():
        registros = promociones.get_all_promociones()
        if not registros:
            return dmc.Alert("No hay promociones registradas.", color="yellow", variant="filled")

        rows = []
        for r in registros:
            # 👇 Formatear fecha
            fecha_str = ""
            if r.get("creado_en"):
                try:
                    fecha_str = datetime.strptime(r["creado_en"][:10], "%Y-%m-%d").strftime("%d/%m/%Y")
                except Exception:
                    fecha_str = r["creado_en"]

            # 👇 Formatear campaña
            campania_label = "-"
            if r.get("campania") and r.get("anio"):
                campania_label = f"C{r['campania']} - {r['anio']}"

            rows.append(
                html.Tr([
                    html.Td(r.get("codigo_padre") or "-"),
                    html.Td(r["nombre"]),
                    html.Td(r["tipo"]),
                    html.Td(campania_label),
                    html.Td(fecha_str),
                    html.Td(
                        dmc.Group([
                            dmc.ActionIcon(
                                DashIconify(icon="tabler:edit", width=18),
                                id={"type": "btn-edit-promocion", "index": r["id"]},
                                color="blue",
                                variant="light"
                            ),
                            dmc.ActionIcon(
                                DashIconify(icon="tabler:trash", width=18),
                                id={"type": "btn-delete-promocion", "index": r["id"]},
                                color="red",
                                variant="light"
                            )
                        ], gap="xs", justify="flex-end")
                    )
                ])
            )

        return dmc.Table(
            [
                html.Thead(html.Tr([
                    html.Th("Código Padre"),
                    html.Th("Nombre"),
                    html.Th("Tipo"),
                    html.Th("Campaña"),
                    html.Th("Creado en"),
                    html.Th("Acciones")
                ])),
                html.Tbody(rows)
            ],
            striped=True,
            highlightOnHover=True,
            withTableBorder=True,
            withRowBorders=True,
            withColumnBorders=True,
            mt=20
        )

    # ---------- Inicializar tabla ----------
    @app.callback(
        Output("tabla-promociones", "children"),
        Input("tabla-promociones", "id")  # dispara al cargar
    )
    def init_tabla(_):
        return render_tabla()

    # ---------- Guardar (Create / Update) ----------
    @app.callback(
        Output("tabla-promociones", "children", allow_duplicate=True),
        Output("modal-promocion", "opened", allow_duplicate=True),
        Output("input-nombre-promocion", "value", allow_duplicate=True),
        Output("select-tipo-promocion", "value", allow_duplicate=True),
        Output("input-codigo-padre", "value", allow_duplicate=True),
        Output("select-campania-promocion", "value", allow_duplicate=True),
        Output("hidden-id-promocion", "value", allow_duplicate=True),
        Input("btn-save-promocion", "n_clicks"),
        State("input-nombre-promocion", "value"),
        State("select-tipo-promocion", "value"),
        State("input-codigo-padre", "value"),
        State("select-campania-promocion", "value"),
        State("hidden-id-promocion", "value"),
        prevent_initial_call=True
    )
    def guardar(n_clicks, nombre, tipo, codigo_padre, id_campania, hidden_id):
        if not n_clicks:
            return no_update, False, no_update, no_update, no_update, no_update, no_update

        if not nombre or not tipo or not id_campania:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update

        if hidden_id:  # UPDATE
            promociones.actualizar_promocion(hidden_id, {
                "nombre": nombre,
                "tipo": tipo,
                "codigo_padre": codigo_padre,
                "id_campania": id_campania
            })
        else:  # INSERT
            promociones.crear_promocion(nombre, tipo, codigo_padre, id_campania)

        return render_tabla(), False, "", None, None, None, None

    # ---------- Eliminar ----------
    @app.callback(
        Output("tabla-promociones", "children", allow_duplicate=True),
        Input({"type": "btn-delete-promocion", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def eliminar(delete_clicks):
        trigger = ctx.triggered_id
        if not trigger or not isinstance(trigger, dict) or trigger.get("type") != "btn-delete-promocion":
            return no_update

        idx = trigger.get("index")
        if not idx:
            return no_update
        pos = [i for i, n in enumerate(delete_clicks) if n and n > 0]
        if not pos:
            return no_update

        promociones.eliminar_promocion(idx)
        return render_tabla()

    # ---------- Abrir modal "nuevo" ----------
    @app.callback(
        Output("modal-promocion", "opened", allow_duplicate=True),
        Output("input-nombre-promocion", "value", allow_duplicate=True),
        Output("select-tipo-promocion", "value", allow_duplicate=True),
        Output("input-codigo-padre", "value", allow_duplicate=True),
        Output("select-campania-promocion", "value", allow_duplicate=True),
        Output("hidden-id-promocion", "value", allow_duplicate=True),
        Input("btn-nueva-promocion", "n_clicks"),
        prevent_initial_call=True
    )
    def open_modal_new(n_clicks):
        return True, "", None, None, None, ""

    # ---------- Abrir modal "editar" ----------
    @app.callback(
        Output("modal-promocion", "opened", allow_duplicate=True),
        Output("input-nombre-promocion", "value", allow_duplicate=True),
        Output("select-tipo-promocion", "value", allow_duplicate=True),
        Output("input-codigo-padre", "value", allow_duplicate=True),
        Output("select-campania-promocion", "value", allow_duplicate=True),
        Output("hidden-id-promocion", "value", allow_duplicate=True),
        Input({"type": "btn-edit-promocion", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def open_modal_edit(edit_clicks):
        trigger = ctx.triggered_id
        if not trigger or not isinstance(trigger, dict) or trigger.get("type") != "btn-edit-promocion":
            return no_update, no_update, no_update, no_update, no_update, no_update

        idx = trigger.get("index")
        if not idx:
            return no_update, no_update, no_update, no_update, no_update, no_update
        pos = [i for i, n in enumerate(edit_clicks) if n and n > 0]
        if not pos:
            return no_update, no_update, no_update, no_update, no_update, no_update

        registro = promociones.get_promocion(idx)
        return True, registro["nombre"], registro["tipo"], registro.get("codigo_padre"), registro.get("id_campania"), registro["id"]

    # ---------- Cancelar modal ----------
    @app.callback(
        Output("modal-promocion", "opened", allow_duplicate=True),
        Input("btn-cancelar-promocion", "n_clicks"),
        prevent_initial_call=True
    )
    def close_modal(_):
        return False

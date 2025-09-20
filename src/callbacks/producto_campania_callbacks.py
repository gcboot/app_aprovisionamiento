from dash import Input, Output, State, ALL, html, ctx, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from src.models import producto_campania, campanias


def register_producto_campania_callbacks(app):

    # ---------- Renderizar tabla ----------
    def render_tabla():
        registros = producto_campania.get_all_producto_campania()
        if not registros:
            return dmc.Alert("No hay registros.", color="yellow", variant="filled")

        rows = []
        for r in registros:
            rows.append(
                html.Tr([
                    html.Td(r["codigo"]),
                    html.Td(r["producto"]),
                    html.Td(f"C{r['campania']} - {r['anio']}"),
                    html.Td(f"Q{r['precio_oferta']:.2f}"),
                    html.Td(
                        dmc.Group([
                            dmc.ActionIcon(
                                DashIconify(icon="tabler:edit", width=18),
                                color="blue",
                                variant="light",
                                id={"type": "btn-edit", "index": f"{r['codigo']}|{r['campania']}|{r['anio']}"}
                            ),
                            dmc.ActionIcon(
                                DashIconify(icon="tabler:trash", width=18),
                                color="red",
                                variant="light",
                                id={"type": "btn-delete", "index": f"{r['codigo']}|{r['campania']}|{r['anio']}"}
                            ),
                        ])
                    )
                ])
            )

        return dmc.Table(
            [
                html.Thead(html.Tr([
                    html.Th("Código"),
                    html.Th("Producto"),
                    html.Th("Campaña"),
                    html.Th("Precio Oferta"),
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
        Output("tabla-producto-campania", "children"),
        Input("tabla-producto-campania", "id")  # dispara al cargar
    )
    def init_tabla(_):
        return render_tabla()

    # ---------- Guardar (Create / Update) ----------
    @app.callback(
        Output("tabla-producto-campania", "children", allow_duplicate=True),
        Output("modal-pc", "opened", allow_duplicate=True),
        Output("hidden-codigo", "value", allow_duplicate=True),
        Output("hidden-id-campania", "value", allow_duplicate=True),
        Output("select-producto", "value", allow_duplicate=True),
        Output("select-campania", "value", allow_duplicate=True),
        Output("input-precio", "value", allow_duplicate=True),
        Input("btn-save-pc", "n_clicks"),
        State("select-producto", "value"),
        State("select-campania", "value"),   # UUID
        State("input-precio", "value"),
        State("hidden-codigo", "value"),
        State("hidden-id-campania", "value"),
        prevent_initial_call=True
    )
    def save_pc(n_clicks, producto, id_campania, precio, hidden_codigo, hidden_id_campania):
        if not n_clicks:
            return no_update, False, no_update, no_update, no_update, no_update, no_update

        # Validar datos mínimos
        if not producto or not id_campania or precio is None:
            print("❌ Datos incompletos:", producto, id_campania, precio)
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update

        try:
            codigo = int(producto)         # producto sigue siendo int
            id_camp = str(id_campania)     # id_campania es UUID string
            precio_val = float(precio)
        except Exception as e:
            print("❌ Error de conversión:", e)
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update

        # UPDATE o INSERT
        if hidden_codigo and hidden_id_campania:
            print("🔄 UPDATE:", codigo, id_camp, precio_val)
            producto_campania.update_producto_campania(codigo, id_camp, precio_val)
        else:
            print("➕ INSERT:", codigo, id_camp, precio_val)
            producto_campania.insert_producto_campania(codigo, id_camp, precio_val)

        # 👇 Refrescar tabla, cerrar modal y resetear todos los campos
        return render_tabla(), False, "", "", None, None, None

    # ---------- Eliminar ----------
    @app.callback(
        Output("tabla-producto-campania", "children", allow_duplicate=True),
        Input({"type": "btn-delete", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def delete_pc(delete_clicks):
        trigger = ctx.triggered_id

        if not trigger or not isinstance(trigger, dict) or trigger.get("type") != "btn-delete":
            return no_update

        idx = trigger.get("index")
        if not idx:
            return no_update
        btn_pos = [i for i, n in enumerate(delete_clicks) if n and n > 0]
        if not btn_pos:
            return no_update

        # Ejecutar delete
        codigo, campania, anio = idx.split("|")
        id_campania = campanias.get_id_by_campania_anio(campania, anio)
        if id_campania:
            print("🗑 DELETE:", codigo, id_campania)
            producto_campania.delete_producto_campania(int(codigo), str(id_campania))

        return render_tabla()

    # ---------- Abrir modal "nuevo" ----------
    @app.callback(
        Output("modal-pc", "opened", allow_duplicate=True),
        Output("hidden-codigo", "value", allow_duplicate=True),
        Output("hidden-id-campania", "value", allow_duplicate=True),
        Output("select-producto", "value", allow_duplicate=True),
        Output("select-campania", "value", allow_duplicate=True),
        Output("input-precio", "value", allow_duplicate=True),
        Input("btn-open-modal", "n_clicks"),
        prevent_initial_call=True
    )
    def open_modal_new(n_clicks):
        return True, "", "", None, None, None

    # ---------- Abrir modal "editar" ----------
    @app.callback(
        Output("modal-pc", "opened", allow_duplicate=True),
        Output("hidden-codigo", "value", allow_duplicate=True),
        Output("hidden-id-campania", "value", allow_duplicate=True),
        Output("select-producto", "value", allow_duplicate=True),
        Output("select-campania", "value", allow_duplicate=True),
        Output("input-precio", "value", allow_duplicate=True),
        Input({"type": "btn-edit", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def open_modal_edit(edit_clicks):
        trigger = ctx.triggered_id

        # ✅ Validar que realmente hubo click en un botón edit
        if (
            not trigger
            or not isinstance(trigger, dict)
            or trigger.get("type") != "btn-edit"
        ):
            return no_update, no_update, no_update, no_update, no_update, no_update

        # Confirmar que el botón presionado tiene n_clicks > 0
        idx = trigger.get("index")
        if not idx:
            return no_update, no_update, no_update, no_update, no_update, no_update
        pos = [i for i, n in enumerate(edit_clicks) if n and n > 0]
        if not pos:
            return no_update, no_update, no_update, no_update, no_update, no_update

        # Extraer datos del botón edit clicado
        codigo, campania, anio = idx.split("|")
        id_campania = campanias.get_id_by_campania_anio(campania, anio)

        registros = producto_campania.get_all_producto_campania()
        pc = next(
            (r for r in registros if str(r["codigo"]) == codigo
             and str(r["campania"]) == campania
             and str(r["anio"]) == anio),
            None
        )

        if pc and id_campania:
            return True, str(codigo), str(id_campania), str(codigo), str(id_campania), pc["precio_oferta"]

        return no_update, no_update, no_update, no_update, no_update, no_update

    # ---------- Cancelar modal ----------
    @app.callback(
        Output("modal-pc", "opened", allow_duplicate=True),
        Input("btn-close-modal", "n_clicks"),
        prevent_initial_call=True
    )
    def close_modal(n_clicks):
        return False

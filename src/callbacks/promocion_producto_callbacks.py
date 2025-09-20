from dash import Input, Output, State, ALL, html, ctx, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from src.models import promocion_producto
from src.core.db import supabase


# ---------- Renderizar tabla ----------
def render_tabla():
    registros = promocion_producto.get_promocion_productos()
    if not registros:
        return dmc.Alert(
            "No hay registros de promociones-productos.",
            color="yellow",
            variant="filled",
            radius="md",
            mt=10
        )

    rows = []
    for r in registros:
        id_index = f"{r['id_promocion']}_{r['codigo']}"
        rows.append(
            html.Tr([
                html.Td(r["promocion"] or "-"),   # nombre promoción
                html.Td(r["codigo"]),             # código producto
                html.Td(r["producto"] or "-"),    # nombre producto
                html.Td(f"Q{r['precio_base']:.2f}" if r.get("precio_base") else "-"),
                html.Td(r["cantidad"]),
                html.Td(
                    dmc.Group([
                        dmc.ActionIcon(
                            DashIconify(icon="tabler:edit", width=20),
                            id={"type": "btn-edit-promocion-producto", "index": id_index},
                            variant="light",
                            color="blue"
                        ),
                        dmc.ActionIcon(
                            DashIconify(icon="tabler:trash", width=20),
                            id={"type": "btn-delete-promocion-producto", "index": id_index},
                            variant="light",
                            color="red"
                        )
                    ], gap="sm", justify="center")
                )
            ])
        )

    return dmc.Table(
        children=[
            html.Thead(html.Tr([
                html.Th("Promoción"),
                html.Th("Código Producto"),
                html.Th("Producto"),
                html.Th("Precio Base"),
                html.Th("Cantidad"),
                html.Th("Acciones")
            ])),
            html.Tbody(rows)
        ],
        highlightOnHover=True,
        withTableBorder=True,   # ✅ compatible con v2.2.1
        withColumnBorders=True,
        striped=True,
        mt=10,
        mb=20,
    )


# ---------- Registrar callbacks ----------
def register_promocion_producto_callbacks(app):
    print("✅ Callbacks de Promoción–Producto registrados")

    # ---------- Guardar / Eliminar ----------
    @app.callback(
        Output("tabla-promocion-producto", "children"),
        Output("promocion_producto_notificacion", "children"),
        Input("btn-save-promocion-producto", "n_clicks"),
        Input({"type": "btn-delete-promocion-producto", "index": ALL}, "n_clicks"),
        State("select-promocion", "value"),
        State("select-producto", "value"),
        State("input-cantidad", "value"),
        State("hidden-id-promocion", "value"),
        State("hidden-codigo", "value"),
        prevent_initial_call=True
    )
    def crud(n_save, n_delete, id_promocion, codigo, cantidad, hidden_promocion, hidden_codigo):
        triggered = ctx.triggered_id

        # Eliminar
        if isinstance(triggered, dict) and triggered["type"] == "btn-delete-promocion-producto":
            id_promocion, codigo = triggered["index"].split("_")
            promocion_producto.delete_promocion_producto(id_promocion, int(codigo))
            return render_tabla(), dmc.Alert("✅ Registro eliminado con éxito.", color="green", variant="filled")

        # Guardar (insert/update)
        if triggered == "btn-save-promocion-producto":
            if not id_promocion or not codigo:
                return render_tabla(), dmc.Alert("⚠️ Debes seleccionar promoción y producto.", color="red", variant="filled")

            if cantidad is None or cantidad < 1:
                return render_tabla(), dmc.Alert("⚠️ La cantidad debe ser mayor o igual a 1.", color="red", variant="filled")

            if hidden_promocion and hidden_codigo:  # UPDATE
                promocion_producto.update_promocion_producto(id_promocion, int(codigo), cantidad)
                msg = dmc.Alert("✅ Registro actualizado con éxito.", color="green", variant="filled")
            else:  # INSERT
                promocion_producto.insert_promocion_producto(id_promocion, int(codigo), cantidad)
                msg = dmc.Alert("✅ Registro creado con éxito.", color="green", variant="filled")

            return render_tabla(), msg

        return no_update, no_update

    # ---------- Abrir / Cerrar modal ----------
    @app.callback(
        Output("modal-promocion-producto", "opened"),
        Output("select-promocion", "value"),
        Output("select-producto", "value"),
        Output("input-cantidad", "value"),
        Output("hidden-id-promocion", "value"),
        Output("hidden-codigo", "value"),
        Input("btn-add-promocion-producto", "n_clicks"),
        Input("btn-close-promocion-producto", "n_clicks"),
        Input({"type": "btn-edit-promocion-producto", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def abrir_cerrar_modal(n_add, n_close, n_edit):
        triggered = ctx.triggered_id

        # Nuevo
        if triggered == "btn-add-promocion-producto":
            return True, None, None, 1, None, None

        # Cerrar
        if triggered == "btn-close-promocion-producto":
            return False, no_update, no_update, no_update, no_update, no_update

        # Editar
        if isinstance(triggered, dict) and triggered["type"] == "btn-edit-promocion-producto":
            id_promocion, codigo = triggered["index"].split("_")
            reg = promocion_producto.get_promocion_producto(id_promocion, int(codigo))
            if not reg:
                return no_update, no_update, no_update, no_update, no_update, no_update

            return (
                True,
                reg.get("id_promocion"),
                str(reg.get("codigo")),   # ✅ cast a string para Select
                reg.get("cantidad"),
                reg.get("id_promocion"),
                str(reg.get("codigo"))
            )

        return no_update, no_update, no_update, no_update, no_update, no_update

    # ---------- Cargar selects ----------
    @app.callback(
        Output("select-promocion", "data"),
        Output("select-producto", "data"),
        Input("modal-promocion-producto", "opened"),
        prevent_initial_call=True
    )
    def cargar_selects(opened):
        if not opened:
            return no_update, no_update

        # Promociones
        promos = supabase.table("promociones").select("id, nombre").execute().data or []
        promociones_data = [{"value": p["id"], "label": p["nombre"]} for p in promos]

        # Productos
        prods = supabase.table("productos").select("codigo, nombre, precio_base").execute().data or []
        productos_data = [{"value": str(p["codigo"]), "label": f"{p['nombre']} (Q{p['precio_base']})"} for p in prods]

        return promociones_data, productos_data

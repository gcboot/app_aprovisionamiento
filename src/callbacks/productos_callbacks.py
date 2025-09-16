from dash import Input, Output, State, ALL, ctx, no_update, html
import dash_mantine_components as dmc
from src.models import productos
from src.core.db import supabase

def register_productos_callbacks(app):

    # ---------- Renderizar tabla ----------
    def render_tabla_productos():
        prods = productos.get_productos()
        if not prods:
            return dmc.Alert("No hay productos registrados.", color="yellow", variant="filled", radius="md", mt=10)

        rows = [
            html.Tr([
                html.Td(prod["codigo"]),
                html.Td(prod["nombre"]),
                html.Td(f"Q{prod.get('precio_base', 0):,.2f}" if prod.get("precio_base") else ""),
                html.Td("Original" if prod.get("es_original") else "Ofertado"),
                html.Td(prod.get("id_categoria") or "-"),
                html.Td(
                    dmc.Group([
                        dmc.Button("Editar", color="blue", size="xs", variant="light",
                                   id={"type": "btn-edit-producto", "index": prod["id"]}),
                        dmc.Button("Eliminar", color="red", size="xs", variant="outline",
                                   id={"type": "btn-del-producto", "index": prod["id"]}),
                    ], gap="sm", justify="flex-end"),
                    style={"textAlign": "center"},
                ),
            ])
            for prod in prods
        ]

        return dmc.Table(
            children=[
                html.Thead(html.Tr([
                    html.Th("Código"),
                    html.Th("Nombre"),
                    html.Th("Precio Base"),
                    html.Th("Tipo"),
                    html.Th("Categoría"),
                    html.Th("Acciones", style={"textAlign": "right"}),
                ]), style={"backgroundColor": "#f5f6fa"}),
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
        Output("productos_tabla", "children"),
        Input("productos_btn_add", "n_clicks"),
        Input("productos_trigger_refresh", "data"),
        Input({"type": "btn-del-producto", "index": ALL}, "n_clicks"),
        prevent_initial_call=False,
    )
    def actualizar_tabla_productos(_, refresh_trigger, __):
        triggered = ctx.triggered_id
        if isinstance(triggered, dict) and "index" in triggered:
            productos.delete_producto(triggered["index"])
        return render_tabla_productos()

    # ---------- Mostrar/Ocultar campo de producto original ----------
    @app.callback(
        Output("productos_original_container", "style"),
        Input("productos_input_es_original", "value")
    )
    def toggle_original_select(es_original):
        if es_original == "false":  # ofertado
            return {"display": "block"}
        return {"display": "none"}

    # ---------- Cargar lista de productos originales ----------
    @app.callback(
        Output("productos_input_original", "data"),
        Input("productos_input_es_original", "value")
    )
    def cargar_productos_originales(es_original):
        if es_original == "false":
            originales = productos.get_productos_originales()
            return [
                {"label": str(p["codigo"]), "value": p["id"]}
                for p in originales
            ]
        return []

    # ---------- Manejar modal (crear / editar / guardar) ----------
    @app.callback(
        Output("productos_modal", "opened"),
        Output("productos_input_codigo", "value"),
        Output("productos_input_nombre", "value"),
        Output("productos_input_precio", "value"),
        Output("productos_input_es_original", "value"),
        Output("productos_input_categoria", "value"),
        Output("productos_input_original", "value"),
        Output("productos_edit_id", "data"),
        Output("productos_notificacion", "children"),
        Output("productos_trigger_refresh", "data"),
        Input("productos_btn_add", "n_clicks"),
        Input({"type": "btn-edit-producto", "index": ALL}, "n_clicks"),
        Input("productos_btn_save", "n_clicks"),
        State("productos_input_codigo", "value"),
        State("productos_input_nombre", "value"),
        State("productos_input_precio", "value"),
        State("productos_input_es_original", "value"),
        State("productos_input_categoria", "value"),
        State("productos_input_original", "value"),
        State("productos_edit_id", "data"),
        prevent_initial_call=True,
    )
    def manejar_modal_productos(n_crear, n_editar, n_guardar,
                                codigo, nombre, precio, es_original, categoria, original_id, edit_id):
        triggered = ctx.triggered_id

        # ➕ CREAR
        if triggered == "productos_btn_add":
            return True, "", "", "", "", "", None, None, no_update, no_update

        # ✏️ EDITAR
        if isinstance(triggered, dict) and "index" in triggered and n_editar and any(n_editar):
            prod = next((p for p in productos.get_productos() if p["id"] == triggered["index"]), None)
            if prod:
                return (
                    True,
                    prod["codigo"],
                    prod["nombre"],
                    prod.get("precio_base", ""),
                    "true" if prod.get("es_original") else "false",  # bool → string
                    prod.get("id_categoria", ""),
                    None,
                    prod["id"],
                    no_update,
                    no_update,
                )

        # 💾 GUARDAR
        if triggered == "productos_btn_save":
            if not nombre or not codigo:
                return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                       dmc.Alert("⚠️ Nombre y código son obligatorios",
                                 color="red", variant="filled", radius="md", mt=10), no_update

            # --- Validar categoría ---
            if categoria:
                cat = supabase.table("categorias").select("id").eq("id", categoria).execute().data
                if not cat:
                    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                           dmc.Alert(
                               f"⚠️ La categoría con ID {categoria} no existe",
                               color="red", variant="filled", radius="md", mt=10
                           ), no_update

            # convertir string → bool
            es_original_bool = True if es_original == "true" else False

            if edit_id:  # actualizar
                productos.update_producto(edit_id, codigo, nombre, precio,
                                          es_original_bool, categoria)
                mensaje = "✅ Producto actualizado con éxito"
                new_id = edit_id
            else:  # insertar
                inserted = supabase.table("productos").insert({
                    "codigo": codigo,
                    "nombre": nombre,
                    "precio_base": precio,
                    "es_original": es_original_bool,
                    "id_categoria": categoria
                }).execute().data
                new_id = inserted[0]["id"] if inserted else None
                mensaje = "✅ Producto creado con éxito"

            # Relacionar si es ofertado
            if es_original == "false" and original_id and new_id:
                supabase.table("producto_oferta").insert({
                    "id_oferta": new_id,
                    "id_original": original_id
                }).execute()

            return False, "", "", "", "", "", None, None, \
                   dmc.Alert(mensaje, color="green", variant="filled", radius="md", mt=10), True

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

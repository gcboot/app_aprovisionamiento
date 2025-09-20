# from dash import Input, Output, State, html, ctx, no_update
# import dash_mantine_components as dmc
# from dash_iconify import DashIconify
# from src.models import promocion_producto, productos


# def register_promocion_producto_callbacks(app):

#     # ---------- Renderizar tabla ----------
#     def render_tabla():
#         registros = promocion_producto.get_all_promocion_producto()
#         if not registros:
#             return dmc.Alert("No hay registros de promociones-productos.", color="yellow", variant="filled")

#         rows = []
#         for r in registros:
#             rows.append(
#                 html.Tr([
#                     html.Td(r["id_promocion"]),
#                     html.Td(r["promociones"]["nombre"] if r.get("promociones") else "-"),
#                     html.Td(r["codigo"]),
#                     html.Td(r["productos"]["nombre"] if r.get("productos") else "-"),
#                     html.Td(r["cantidad"]),
#                     html.Td(
#                         dmc.Group([
#                             dmc.ActionIcon(
#                                 DashIconify(icon="tabler:edit", width=20),
#                                 id={"type": "btn-edit-promocion-producto", "index": f'{r["id_promocion"]}_{r["codigo"]}'},
#                                 variant="light",
#                                 color="blue"
#                             ),
#                             dmc.ActionIcon(
#                                 DashIconify(icon="tabler:trash", width=20),
#                                 id={"type": "btn-delete-promocion-producto", "index": f'{r["id_promocion"]}_{r["codigo"]}'},
#                                 variant="light",
#                                 color="red"
#                             )
#                         ])
#                     )
#                 ])
#             )

#         return dmc.Table(
#             children=[
#                 html.Thead(html.Tr([
#                     html.Th("ID Promoción"),
#                     html.Th("Promoción"),
#                     html.Th("Código Producto"),
#                     html.Th("Producto"),
#                     html.Th("Cantidad"),
#                     html.Th("Acciones")
#                 ])),
#                 html.Tbody(rows)
#             ],
#             highlightOnHover=True,
#             withBorder=True,
#             withColumnBorders=True,
#             striped=True
#         )

#     # ---------- Callback para renderizar tabla ----------
#     @app.callback(
#         Output("tabla-promocion-producto", "children"),
#         Input("refresh-promocion-producto", "n_clicks"),
#         prevent_initial_call=True
#     )
#     def actualizar_tabla(_):
#         return render_tabla()

#     # ---------- Guardar (INSERT / UPDATE) ----------
#     @app.callback(
#         Output("modal-promocion-producto", "opened"),
#         Output("refresh-promocion-producto", "n_clicks"),
#         Input("btn-save-promocion-producto", "n_clicks"),
#         State("select-promocion", "value"),
#         State("select-producto", "value"),
#         State("input-cantidad", "value"),
#         State("hidden-id-promocion", "value"),
#         State("hidden-codigo", "value"),
#         prevent_initial_call=True
#     )
#     def guardar(n_clicks, id_promocion, codigo, cantidad, hidden_promocion, hidden_codigo):
#         if not id_promocion or not codigo:
#             return no_update, no_update

#         # Si venían valores hidden → UPDATE
#         if hidden_promocion and hidden_codigo:
#             promocion_producto.actualizar_promocion_producto(id_promocion, codigo, cantidad)
#         else:
#             promocion_producto.crear_promocion_producto(id_promocion, codigo, cantidad)

#         return False, 1  # cerrar modal y refrescar tabla

#     # ---------- Editar ----------
#     @app.callback(
#         Output("modal-promocion-producto", "opened"),
#         Output("select-promocion", "value"),
#         Output("select-producto", "value"),
#         Output("input-cantidad", "value"),
#         Output("hidden-id-promocion", "value"),
#         Output("hidden-codigo", "value"),
#         Input({"type": "btn-edit-promocion-producto", "index": str}, "n_clicks"),
#         prevent_initial_call=True
#     )
#     def editar(n_clicks, btn_id):
#         if not n_clicks:
#             return no_update, no_update, no_update, no_update, no_update, no_update

#         id_promocion, codigo = btn_id.split("_")
#         registro = promocion_producto.get_promocion_producto(id_promocion, int(codigo))

#         return True, registro["id_promocion"], registro["codigo"], registro["cantidad"], registro["id_promocion"], registro["codigo"]

#     # ---------- Eliminar ----------
#     @app.callback(
#         Output("refresh-promocion-producto", "n_clicks"),
#         Input({"type": "btn-delete-promocion-producto", "index": str}, "n_clicks"),
#         prevent_initial_call=True
#     )
#     def eliminar(n_clicks, btn_id):
#         if not n_clicks:
#             return no_update

#         id_promocion, codigo = btn_id.split("_")
#         promocion_producto.eliminar_promocion_producto(id_promocion, int(codigo))
#         return 1

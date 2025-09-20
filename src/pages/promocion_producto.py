# import dash
# from dash import html, dcc
# import dash_mantine_components as dmc
# from dash_iconify import DashIconify
# from src.models import promocion_producto, productos

# dash.register_page(
#     __name__,
#     path="/home/promocion_producto",
#     name="Promoción-Producto"
# )


# def layout():
#     # Opciones dinámicas para selects
#     opciones_promociones = [
#         {"value": p["id"], "label": f'{p["nombre"]} ({p["tipo"]})'}
#         for p in promocion_producto.get_all_promociones()
#     ]

#     opciones_productos = [
#         {"value": p["codigo"], "label": f'{p["codigo"]} - {p["nombre"]}'}
#         for p in productos.get_productos()
#     ]

#     return dmc.Container([
#         dmc.Group([
#             dmc.Title("Promoción - Producto", order=2),
#             dmc.Button(
#                 "Nueva Relación",
#                 id="btn-nuevo-promocion-producto",
#                 leftSection=DashIconify(icon="tabler:plus"),
#                 color="blue",
#                 radius="md"
#             ),
#         ], justify="space-between", mb=20),

#         # ---------- Tabla ----------
#         html.Div(id="tabla-promocion-producto"),
#         dcc.Store(id="refresh-promocion-producto"),

#         # ---------- Modal ----------
#         dmc.Modal(
#             id="modal-promocion-producto",
#             opened=False,
#             title="Asignar producto a promoción",
#             size="lg",
#             centered=True,
#             children=[
#                 # Hidden fields para edición
#                 dcc.Store(id="hidden-id-promocion"),
#                 dcc.Store(id="hidden-codigo"),

#                 dmc.Select(
#                     id="select-promocion",
#                     label="Promoción",
#                     placeholder="Selecciona una promoción",
#                     data=opciones_promociones,
#                     searchable=True,
#                     required=True,
#                     mb=15
#                 ),
#                 dmc.Select(
#                     id="select-producto",
#                     label="Producto",
#                     placeholder="Selecciona un producto",
#                     data=opciones_productos,
#                     searchable=True,
#                     required=True,
#                     mb=15
#                 ),
#                 dmc.NumberInput(
#                     id="input-cantidad",
#                     label="Cantidad",
#                     value=1,
#                     min=1,
#                     step=1,
#                     required=True,
#                     mb=25
#                 ),
#                 dmc.Button(
#                     "Guardar",
#                     id="btn-save-promocion-producto",
#                     fullWidth=True,
#                     color="blue",
#                     radius="md",
#                     size="md"
#                 )
#             ]
#         )
#     ], fluid=True)

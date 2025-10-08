import dash
from dash import html, dcc
import dash_mantine_components as dmc
from src.components.layout_base import layout_base
from src.callbacks.promocion_producto_callbacks import render_tabla

# Registrar página
dash.register_page(__name__, path="/home/promocion_producto", name="Promoción–Producto")

# Layout de la página
layout = layout_base(
    dmc.Stack([

        # Botón para agregar producto a promoción
        dmc.Button(
            "➕ Agregar a Promoción",
            id="btn-add-promocion-producto",
            color="teal",
            variant="filled",
            radius="md",
            size="sm",
            style={"width": "220px", "marginBottom": "10px"}
        ),

        # Mensajes de notificación
        html.Div(id="promocion_producto_notificacion"),

        # Tabla de promoción-producto (render inicial directo)
        html.Div(render_tabla(), id="tabla-promocion-producto"),

        # Modal CRUD Promoción–Producto
        dmc.Modal(
            id="modal-promocion-producto",
            opened=False,
            title="Asignar Producto a Promoción",
            centered=True,
            size="lg",
            overlayProps={"opacity": 0.55, "blur": 3},
            children=[

                # Select dinámicos (se llenan desde callback cargar_selects)
                dmc.Select(
                    id="select-promocion",
                    label="Promoción",
                    placeholder="Seleccione promoción",
                    data=[],   # Se llena dinámicamente
                    searchable=True,
                    nothingFoundMessage="No se encontró promoción",
                    mb=10
                ),
                dmc.Select(
                    id="select-producto",
                    label="Producto",
                    placeholder="Seleccione producto",
                    data=[],   # Se llena dinámicamente
                    searchable=True,
                    nothingFoundMessage="No se encontró producto",
                    mb=10
                ),

                # Cantidad
                dmc.NumberInput(
                    id="input-cantidad",
                    label="Cantidad",
                    required=True,
                    min=1,
                    step=1,
                    value=1,
                    radius="md",
                    mb=20
                ),

                # Botones de acción
                dmc.Group(
                    [
                        dmc.Button(
                            "Cancelar",
                            id="btn-close-promocion-producto",
                            color="red",
                            variant="light",
                            radius="md"
                        ),
                        dmc.Button(
                            "Guardar",
                            id="btn-save-promocion-producto",
                            color="blue",
                            radius="md"
                        )
                    ],
                    justify="flex-end",   # ✅ Compatible con dmc 2.2.1
                    mt=10
                )
            ]
        ),

        # Stores auxiliares
        dcc.Store(id="hidden-id-promocion"),
        dcc.Store(id="hidden-codigo")
    ]),
    titulo="Mantenimiento Promoción–Producto"
)

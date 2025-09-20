from dash import Input, Output, State, ALL, ctx, no_update, html
import dash_mantine_components as dmc
from src.models import categorias


def register_categorias_callbacks(app):

    # ---------- Renderizar tabla ----------
    def render_tabla():
        cats = categorias.get_categorias()
        if not cats:
            return dmc.Alert(
                "No hay categorías registradas.",
                color="yellow",
                variant="filled",
                radius="md",
                mt=10,
            )

        rows = [
            html.Tr([
                html.Td(cat["nombre"]),
                html.Td(cat.get("descripcion", "")),
                html.Td(
                    dmc.Group(
                        [
                            dmc.Button(
                                "Editar",
                                color="blue",
                                size="xs",
                                variant="light",
                                id={"type": "btn-edit-categoria", "index": cat["id"]},
                            ),
                            dmc.Button(
                                "Eliminar",
                                color="red",
                                size="xs",
                                variant="outline",
                                id={"type": "btn-del-categoria", "index": cat["id"]},
                            ),
                        ],
                        gap="sm",
                        justify="flex-end",
                    ),
                    style={"textAlign": "right"},
                ),
            ])
            for cat in cats
        ]

        return dmc.Table(
            children=[
                html.Thead(
                    html.Tr(
                        [
                            html.Th("Nombre"),
                            html.Th("Descripción"),
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
            style={"borderRadius": "8px", "overflow": "hidden"},
        )

    # ---------- Actualizar tabla ----------
    @app.callback(
        Output("tabla-categorias", "children"),
        Input("btn-add-categoria", "n_clicks"),
        Input("trigger-refresh-categorias", "data"),   # <- store para refrescar
        Input({"type": "btn-del-categoria", "index": ALL}, "n_clicks"),
        prevent_initial_call=False,
    )
    def actualizar_tabla(_, refresh_trigger, __):
        triggered = ctx.triggered_id
        if isinstance(triggered, dict) and "index" in triggered:  # eliminar
            categorias.delete_categoria(triggered["index"])
        return render_tabla()

    # ---------- Manejar modal (crear / editar / guardar) ----------
    @app.callback(
        Output("modal-categoria", "opened"),
        Output("input-nombre-categoria", "value"),
        Output("input-descripcion-categoria", "value"),
        Output("categoria-edit-id", "data"),
        Output("notificacion-categoria", "children"),
        Output("trigger-refresh-categorias", "data"),  # <- dispara refresco
        Input("btn-add-categoria", "n_clicks"),
        Input({"type": "btn-edit-categoria", "index": ALL}, "n_clicks"),
        Input("btn-save-categoria", "n_clicks"),
        State("input-nombre-categoria", "value"),
        State("input-descripcion-categoria", "value"),
        State("categoria-edit-id", "data"),
        prevent_initial_call=True,
    )
    def manejar_modal(n_crear, n_editar, n_guardar, nombre, descripcion, edit_id):
        triggered = ctx.triggered_id

        # ➕ CREAR → abrir modal vacío
        if triggered == "btn-add-categoria":
            return True, "", "", None, no_update, no_update

        # ✏️ EDITAR → abrir modal con datos existentes
        if isinstance(triggered, dict) and "index" in triggered and n_editar and any(n_editar):
            cat = next((c for c in categorias.get_categorias() if c["id"] == triggered["index"]), None)
            if cat:
                return True, cat["nombre"], cat.get("descripcion", ""), cat["id"], no_update, no_update

        # 💾 GUARDAR → insertar o actualizar
        if triggered == "btn-save-categoria":
            if not nombre:
                return (
                    no_update, no_update, no_update, no_update,
                    dmc.Alert(
                        "⚠️ El nombre es obligatorio",
                        color="red",
                        variant="filled",
                        radius="md",
                        mt=10,
                    ),
                    no_update,
                )

            if edit_id:  # actualizar
                categorias.update_categoria(edit_id, nombre, descripcion)
                mensaje = "✅ Categoría actualizada con éxito"
            else:       # insertar
                categorias.insert_categoria(nombre, descripcion)
                mensaje = "✅ Categoría creada con éxito"

            return (
                False, "", "", None,
                dmc.Alert(mensaje, color="green", variant="filled", radius="md", mt=10),
                True,  # refrescar tabla
            )

        # 🔴 DEFAULT → no cambia nada
        return no_update, no_update, no_update, no_update, no_update, no_update

from dash import Output, Input, State, no_update, ALL, ctx
import time
from src.pages.usuarios.lista_helpers import get_usuarios, actualizar_usuario, eliminar_usuario, make_table

def register_lista_callbacks(app):

    # Refrescar tabla de usuarios
    @app.callback(
        Output("tabla-usuarios", "children"),
        [Input("search-usuarios", "value"),
         Input("refresh-store", "data")]
    )
    def refrescar_tabla(search, refresh_data):
        usuarios = get_usuarios()
        if search:
            search_lower = search.lower()
            usuarios = [
                u for u in usuarios
                if search_lower in (u.get("nombre") or "").lower()
                or search_lower in (u.get("correo") or "").lower()
            ]
        return make_table(usuarios)

    # Abrir modal de edición
    @app.callback(
        Output("modal-editar", "opened"),
        Output("edit-user-id", "value"),
        Output("edit-user-nombre", "value"),
        Output("edit-user-correo", "value"),
        Output("edit-user-rol", "value"),
        Input({"type": "btn-editar", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def abrir_modal(n_clicks):
        if not ctx.triggered_id:
            return no_update, no_update, no_update, no_update, no_update

        # ✅ solo abrir si se hizo click en un botón
        clicks = n_clicks or []
        if not any(clicks):
            return no_update, no_update, no_update, no_update, no_update

        user_id = ctx.triggered_id["index"]
        user = next((u for u in get_usuarios() if u["id"] == user_id), None)
        if user:
            return True, user["id"], user.get("nombre", ""), user.get("correo") or "", user.get("rol", "")
        return no_update, no_update, no_update, no_update, no_update

    # Actualizar usuario
    @app.callback(
        Output("edit-message", "children"),
        Output("refresh-store", "data"),
        Input("btn-actualizar-usuario", "n_clicks"),
        State("edit-user-id", "value"),
        State("edit-user-correo", "value"),
        State("edit-user-rol", "value"),
        prevent_initial_call=True
    )
    def actualizar_usuario_callback(n, user_id, correo, rol):
        if not user_id:
            return "❌ Error: no se seleccionó usuario", no_update
        ok = actualizar_usuario(user_id, correo, rol)
        return ("✅ Usuario actualizado", str(int(time.time()))) if ok else ("❌ Error al actualizar", no_update)

    # Eliminar usuario
    @app.callback(
        Output("refresh-store", "data", allow_duplicate=True),
        Input({"type": "btn-eliminar", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def eliminar_usuario_callback(n_clicks):
        if not ctx.triggered_id:
            return no_update

        # ✅ solo eliminar si hay un click real
        clicks = n_clicks or []
        if not any(clicks):
            return no_update

        user_id = ctx.triggered_id["index"]
        ok = eliminar_usuario(user_id)
        return str(int(time.time())) if ok else no_update

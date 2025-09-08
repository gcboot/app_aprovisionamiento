from dash import Output, Input, no_update
from src.core.db import supabase

def register_cerrar_sesion_callbacks(app):
    @app.callback(
        Output("session-store", "data", allow_duplicate=True),  # 👈 permitimos duplicados
        Output("url-redirect", "href"),
        Input("btn-logout", "n_clicks"),
        prevent_initial_call=True
    )
    def logout(n_clicks):
        if not n_clicks:
            return no_update, no_update

        try:
            supabase.auth.sign_out()
        except Exception as e:
            print("❌ Error al cerrar sesión:", e)

        # limpiar sesión y redirigir al login
        return None, "/"

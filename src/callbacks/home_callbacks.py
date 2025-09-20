from dash import Output, Input, no_update

def register_home_callbacks(app):
    @app.callback(
        Output("welcome-message", "children"),
        Input("session-store", "data"),
        prevent_initial_call=False  # se ejecuta al cargar la página
    )
    def mostrar_bienvenida(session_data):
        if not session_data:
            return "Bienvenido"
        nombre = session_data.get("nombre") or "Usuario"
        return f"Bienvenido {nombre}"

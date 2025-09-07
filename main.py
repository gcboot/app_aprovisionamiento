# main.py
import dash
from dash import html, Input, Output, dcc
import dash_mantine_components as dmc
from src.pages.auth import login_layout, register_callbacks
from src.pages.app import main_layout

# =========================
# Inicialización de la app
# =========================
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Plataforma Predictiva"

# =========================
# Layouts pre-generados
# =========================
# Se crean una sola vez para evitar que los inputs se reinicien
LOGIN_PAGE = login_layout()
MAIN_PAGE = main_layout()

# =========================
# Layout base
# =========================
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=html.Div([
        # Memoria de sesión en el navegador
        dcc.Store(id="session-store", storage_type="local"),

        # Aquí se inyecta login o dashboard
        html.Div(id="page-content")
    ])
)

# =========================
# Callbacks
# =========================

# Decidir qué mostrar: login o dashboard
@app.callback(
    Output("page-content", "children"),
    Input("session-store", "data"),
    prevent_initial_call=False
)
def mostrar_pagina(session_data):
    """
    Renderiza login si no hay sesión activa,
    o el dashboard si existe usuario logueado.
    """
    if session_data and "usuario_id" in session_data:
        return MAIN_PAGE
    return LOGIN_PAGE

# Cerrar sesión → limpia el store y vuelve al login
@app.callback(
    Output("session-store", "clear_data"),
    Input("btn-logout", "n_clicks"),
    prevent_initial_call=True
)
def cerrar_sesion(n_clicks):
    """
    Limpia la sesión en el navegador al presionar el botón de logout.
    """
    if n_clicks:
        return True

# Registrar callbacks del login (procesar credenciales, etc.)
register_callbacks(app)

# =========================
# Ejecutar servidor
# =========================
if __name__ == "__main__":
    app.run(debug=True)
    
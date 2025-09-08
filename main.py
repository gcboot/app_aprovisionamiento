from dash import Dash, html, dcc
import dash
import dash_mantine_components as dmc
from src.callbacks.auth_callbacks import register_auth_callbacks
from src.callbacks.lista_callbacks import register_lista_callbacks
from src.callbacks.cerrar_sesion_callbacks import register_cerrar_sesion_callbacks
from src.callbacks.home_callbacks import register_home_callbacks

app = Dash(
    __name__,
    use_pages=True,
    pages_folder="src/pages",
    suppress_callback_exceptions=True
)
server = app.server

app.layout = dmc.MantineProvider(
    children=[
        dcc.Store(id="session-store", storage_type="session"),
        dcc.Location(id="url-redirect", refresh=True),  # 👈 necesario para redirigir tras logout
        dash.page_container
    ]
)

# Registrar callbacks
register_auth_callbacks(app)
register_lista_callbacks(app)
register_cerrar_sesion_callbacks(app)  # 👈 registrar logout
register_home_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)

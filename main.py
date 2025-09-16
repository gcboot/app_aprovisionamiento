from dash import Dash, dcc
import dash
import dash_mantine_components as dmc

# Callbacks existentes
from src.callbacks.auth_callbacks import register_auth_callbacks
from src.callbacks.lista_callbacks import register_lista_callbacks
from src.callbacks.cerrar_sesion_callbacks import register_cerrar_sesion_callbacks
from src.callbacks.home_callbacks import register_home_callbacks
from src.callbacks import categorias_callbacks
from src.callbacks import campanias_callbacks   # 👈 lo puedes crear igual que categorias
from src.callbacks import productos_callbacks


# Callbacks nuevos
from src.callbacks import inventario_callbacks


app = Dash(
    __name__,
    use_pages=True,
    pages_folder="src/pages",
    suppress_callback_exceptions=True
)
server = app.server

# ---------- Layout principal ----------
app.layout = dmc.MantineProvider(
    children=[
        dcc.Store(id="session-store", storage_type="session"),
        dcc.Location(id="url-redirect", refresh=True),  # redirección tras logout
        dash.page_container
    ]
)

# ---------- Registrar callbacks ----------
register_auth_callbacks(app)
register_lista_callbacks(app)
register_cerrar_sesion_callbacks(app)
register_home_callbacks(app)

# nuevos mantenimientos
categorias_callbacks.register_callbacks(app)
campanias_callbacks.register_campanias_callbacks(app)
productos_callbacks.register_productos_callbacks(app)
inventario_callbacks.register_inventario_callbacks(app)


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)

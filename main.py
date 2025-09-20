from dash import Dash, dcc
import dash
import dash_mantine_components as dmc

# Callbacks existentes
from src.callbacks.auth_callbacks import register_auth_callbacks
from src.callbacks.lista_callbacks import register_lista_callbacks
from src.callbacks.cerrar_sesion_callbacks import register_cerrar_sesion_callbacks
from src.callbacks.home_callbacks import register_home_callbacks
from src.callbacks.categorias_callbacks import register_categorias_callbacks
from src.callbacks.productos_callbacks import register_productos_callbacks
from src.callbacks.inventario_callbacks import register_inventario_callbacks
from src.callbacks.producto_campania_callbacks import register_producto_campania_callbacks

# Callbacks nuevos
# from src.callbacks.promocion_producto_callbacks import register_promocion_producto_callbacks




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
register_categorias_callbacks(app)
register_productos_callbacks(app)
register_inventario_callbacks(app)
register_producto_campania_callbacks(app)

# nuevos mantenimientos
# register_promocion_producto_callbacks






# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)

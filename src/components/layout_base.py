from dash import html
import dash_mantine_components as dmc

def sidebar():
    return html.Div(
        className="sidebar",
        children=[
            dmc.Title("Nextlytics", order=3, ta="center", c="blue"),
            dmc.NavLink(label="🏠 Inicio", href="/home", id="nav-home"),            
            dmc.NavLink(label="🤖 Predicciones", href="/home/predicciones", id="nav-predicciones"),
            dmc.NavLink(label="📑 Reportes", href="/home/reportes", id="nav-reportes"),
            dmc.NavLink(label="📋 Inventarios", href="/home/inventario", id="nav-inventario"),
            dmc.NavLink(
                label="👥 Usuarios", 
                children=[
                    dmc.NavLink(label="📋 Lista de Usuarios", href="/home/usuarios/lista", id="nav-usuarios-lista"),
                    dmc.NavLink(label="➕ Crear Usuario", href="/home/usuarios/registro", id="nav-usuarios-crear"),
                ]),
            dmc.NavLink(
                label="🛠️ Mantenimientos", 
                children=[
                    dmc.NavLink(label="Categorías", href="/home/categorias", id="nav-mantenimientos-categorias"),
                    dmc.NavLink(label="Campañas", href="/home/campanias", id="nav-mantenimientos-campanias"),
                    dmc.NavLink(label="Productos", href="/home/productos", id="nav-mantenimientos-productos"),
                ]),
            dmc.Space(h=20),
            dmc.Button("Cerrar Sesión", id="btn-logout", color="red", fullWidth=True),
        ]
    )

def layout_base(content, titulo=None, subtitulo=None):
    """Envuelve el contenido de cada página con el sidebar y encabezados."""
    elementos = []
    if titulo:
        elementos.append(dmc.Title(titulo, order=2, mb=10))
    if subtitulo:
        elementos.append(dmc.Text(subtitulo, c="dimmed", size="sm", mb=20))
    elementos.append(content)

    return html.Div(
        className="dashboard-container",
        children=[
            sidebar(),
            html.Div(className="content", children=elementos)
        ]
    )

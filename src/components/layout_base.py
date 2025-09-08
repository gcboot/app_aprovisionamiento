from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash


def sidebar():
    return html.Div(
        className="sidebar",
        children=[
            dmc.Title("Nextlytics", order=3, ta="center", c="blue"),
            dmc.NavLink(label="🏠 Inicio", href="/home", id="nav-home"),            
            dmc.NavLink(label="🤖 Predicciones", href="/home/predicciones", id="nav-predicciones"),
            dmc.NavLink(label="📑 Reportes", href="/home/reportes", id="nav-reportes"),
            dmc.NavLink(
                label="👥 Usuarios", 
                children =[
                    dmc.NavLink(label="📋 Lista de Usuarios", href="/home/usuarios/lista", id="nav-usuarios-lista"),
                    dmc.NavLink(label="➕ Crear Usuario", href="/home/usuarios/registro", id="nav-usuarios-crear"),
                ]),
            dmc.NavLink(label="⚙️ Configuración", href="/home/config", id="nav-config"),
            dmc.Space(h=20),
            dmc.Button("Cerrar Sesión", id="btn-logout", color="red", fullWidth=True),
        ]
    )


def layout_base(content):
    """Envuelve el contenido de cada página con el sidebar."""
    return html.Div(
        className="dashboard-container",
        children=[
            sidebar(),
            html.Div(className="content", children=[content])
        ]
    )

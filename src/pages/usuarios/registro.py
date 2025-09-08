from src.components.layout_base import layout_base
import dash
from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/home/usuarios/registro", title="Registro de Usuario")

content = dmc.Center(   # 👈 aquí centramos todo
    dmc.Card(
        withBorder=True,
        shadow="xl",
        radius="xl",
        className="login-card",
        style={"maxWidth": "500px"},  # 👈 ancho fijo para centrar mejor
        children=[
            dmc.Title("Crear Usuario", order=2, ta="center"),
            dmc.Space(h=25),

            dmc.TextInput(
                label="Nombre completo",
                placeholder="Juan Pérez",
                leftSection=DashIconify(icon="mdi:account"),
                required=True,
                id="input-nombre"
            ),
            dmc.Space(h=15),

            dmc.TextInput(
                label="Correo electrónico",
                placeholder="usuario@ejemplo.com",
                leftSection=DashIconify(icon="mdi:email"),
                required=True,
                id="input-email-registro"
            ),
            dmc.Space(h=15),

            dmc.PasswordInput(
                label="Contraseña",
                placeholder="********",
                leftSection=DashIconify(icon="mdi:lock"),
                required=True,
                id="input-password-registro"
            ),
            dmc.Space(h=10),

            dmc.Progress(value=0, color="red", id="password-strength-registro"),
            dmc.Text("Contraseña débil", id="password-strength-msg", ta="center", c="red"),
            dmc.Space(h=15),

            dmc.PasswordInput(
                label="Confirmar contraseña",
                placeholder="********",
                leftSection=DashIconify(icon="mdi:lock-check"),
                required=True,
                id="input-confirm-password"
            ),
            dmc.Space(h=15),

            dmc.Select(
                label="Rol",
                data=[
                    {"label": "Administrador", "value": "admin"},
                    {"label": "Analista", "value": "analista"},
                    {"label": "Gerente", "value": "gerente"},
                    {"label": "Cliente", "value": "cliente"},
                ],
                value="cliente",
                id="select-rol"
            ),
            dmc.Space(h=25),

            dmc.Button(
                "Crear Usuario",
                fullWidth=True,
                size="lg",
                radius="md",
                color="blue",
                id="btn-crear-usuario",
                n_clicks=0
            ),
            dmc.Space(h=20),

            dmc.Text(
                "Complete los campos para registrar un usuario",
                id="registro-message",
                ta="center",
                c="gray"
            ),
        ]
    ),
    style={"width": "100%", "marginTop": "40px"}  # 👈 margen superior opcional
)

layout = layout_base(content)

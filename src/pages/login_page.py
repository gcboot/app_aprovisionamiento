import dash
from dash import html, dcc   # 👈 agregamos dcc para redirección
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# Registramos la página multipage
dash.register_page(__name__, path="/", title="Iniciar Sesión")


def login_layout():
    """Layout del formulario de inicio de sesión"""
    return html.Div(   # 👈 corregido (antes estaba tml.Div)
        className="login-container",
        children=[
            # --- Logo ---
            dmc.Center(
                dmc.Image(src="/assets/logo.png", w=250, h=250),
                style={"marginTop": "40px"}
            ),

            # --- Card central ---
            dmc.Card(
                withBorder=True,
                shadow="xl",
                radius="xl",
                className="login-card",
                children=[
                    dmc.Title("Plataforma Predictiva", order=2, ta="center"),
                    dmc.Space(h=25),

                    dmc.TextInput(
                        label="Correo electrónico",
                        placeholder="usuario@ejemplo.com",
                        leftSection=DashIconify(icon="mdi:email"),
                        required=True,
                        id="input-email",
                        inputProps={"type": "email", "autoComplete": "username"}
                    ),
                    dmc.Space(h=15),

                    dmc.PasswordInput(
                        label="Contraseña",
                        placeholder="********",
                        leftSection=DashIconify(icon="mdi:lock"),
                        required=True,
                        id="input-password",
                        inputProps={"autoComplete": "current-password"}
                    ),
                    dmc.Space(h=10),

                    dmc.Progress(value=0, color="red", id="password-strength"),
                    dmc.Space(h=15),

                    dmc.Checkbox(label="Recordar sesión", id="check-remember"),
                    dmc.Space(h=25),

                    dmc.Button(
                        "Iniciar Sesión",
                        fullWidth=True,
                        size="lg",
                        radius="md",
                        color="blue",
                        id="btn-login",
                        n_clicks=0
                    ),
                    dmc.Space(h=20),

                    dmc.Text(
                        "Ingrese sus credenciales",
                        id="login-message",
                        ta="center",
                        c="gray"
                    )
                ]
            ),

            # --- Footer ---
            dmc.Text(
                "© 2024 Victor Cun - Todos los derechos reservados",
                className="footer-text"
            ),

            # --- Store y redirección ---
            dcc.Store(id="session-store", storage_type="session"),
            dcc.Location(id="redirect-home", refresh=True)  # 👈 para ir a /home
        ]
    )


# 👇 Dash multipage exige esta variable
layout = login_layout()

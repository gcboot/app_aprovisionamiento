from dash import html, Input, Output, State, dcc, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from src.core.db import autenticar_usuario, obtener_usuario_por_auth_id, crear_sesion


# =========================
# Layout del Login
# =========================
def login_layout():
    return html.Div(
        style={
            "height": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "space-between",
            "alignItems": "center",
            

        },
        children=[
            # --- Logo arriba ---
            dmc.Center(
                dmc.Image(src="/assets/logo.png", w=250, h=250),
                style={"marginTop": "40px"}
            ),

            # --- Card central (login) ---
            dmc.Card(
                withBorder=True,
                shadow="xl",
                radius="xl",
                style={"width": 420, "padding": 40, "backgroundColor": "white"},
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

            # --- Footer con nombre y derechos ---
            dmc.Text(
                "© 2024 Victor Cun - Todos los derechos reservados",
                ta="center",
                c="gray",
                size="sm",
                style={"marginBottom": "15px"}
            )
        ]
    )


# =========================
# Callbacks del Login   
# =========================
def register_callbacks(app):
    # --- Barra de fuerza de contraseña ---
    @app.callback(
        Output("password-strength", "value"),
        Output("password-strength", "color"),
        Input("input-password", "value"),
    )
    def validar_fuerza_contrasena(contrasena):
        if not contrasena:
            return 0, "red"
        score = 0
        if len(contrasena) >= 8: score += 25
        if any(c.islower() for c in contrasena): score += 25
        if any(c.isupper() for c in contrasena): score += 25
        if any(c.isdigit() for c in contrasena) or any(c in "!@#$%^&*()" for c in contrasena):
            score += 25
        color = "red" if score < 50 else "yellow" if score < 75 else "green"
        return score, color

    # --- Procesar login ---
    @app.callback(
        Output("login-message", "children"),
        Output("login-message", "c"),
        Output("session-store", "data"),
        Output("input-password", "value"),   # limpiamos campo si falla
        Input("btn-login", "n_clicks"),
        Input("input-password", "n_submit"), # login con Enter
        State("input-email", "value"),
        State("input-password", "value"),
        prevent_initial_call=True
    )
    def procesar_login(n_clicks, n_submit, correo, contrasena):
        if not correo or not contrasena:
            return "Debe ingresar correo y contraseña", "red", None, ""

        try:
            # Autenticación contra Supabase Auth
            auth_response = autenticar_usuario(correo, contrasena)

            if not auth_response.user:
                return "Correo o contraseña inválidos", "red", None, ""

            # Datos adicionales desde tabla usuarios
            auth_id = auth_response.user.id
            usuario = obtener_usuario_por_auth_id(auth_id)

            if not usuario.data:
                return "Usuario no registrado en tabla usuarios", "yellow", None, ""

            usuario_id = usuario.data[0]["id"]
            rol = usuario.data[0]["rol"]
            nombre = usuario.data[0]["nombre"]

            # Registrar sesión en BD
            crear_sesion(usuario_id, ip="127.0.0.1", dispositivo="Navegador")

            session_data = {"usuario_id": usuario_id, "nombre": nombre, "rol": rol}
            return f"Bienvenido {nombre} ({rol})", "green", session_data, no_update

        except Exception as e:
            return f"Error en login: {str(e)}", "red", None, ""

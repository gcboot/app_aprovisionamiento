from dash import Input, Output, State, no_update
from src.models import usuario_model, sesion_model


def register_auth_callbacks(app):
    """
    Callbacks relacionados con autenticación:
    - Validación de fuerza de contraseña
    - Login
    - Registro
    """

    # --- Validar fuerza de contraseña en registro ---
    @app.callback(
        Output("password-strength-registro", "value"),
        Output("password-strength-registro", "color"),
        Output("password-strength-msg", "children"),
        Output("password-strength-msg", "c"),
        Input("input-password-registro", "value"),
        prevent_initial_call=True
    )
    def validar_password_strength(password):
        score = usuario_model.evaluar_password_strength(password)
        if score >= 80:
            return score, "green", "Contraseña fuerte ✅", "green"
        elif score >= 50:
            return score, "yellow", "Contraseña media ⚠️", "orange"
        else:
            return score, "red", "Contraseña débil ❌", "red"

    # --- LOGIN ---
    @app.callback(
        Output("login-message", "children"),
        Output("session-store", "data"),
        Output("redirect-home", "href"),
        Input("btn-login", "n_clicks"),
        State("input-email", "value"),
        State("input-password", "value"),
        prevent_initial_call=True
    )
    def login(n, email, password):
        if not email or not password:
            return "⚠️ Ingrese sus credenciales", no_update, no_update

        resp = usuario_model.login_usuario(email, password)

        if resp.user:  # ✅ login exitoso
            return (
                f"Bienvenido ✅ {resp.user.email}",
                sesion_model.guardar_sesion(resp.user.id, "cliente"),  # 👈 aquí podrías usar el rol real
                "/home"
            )

        if resp.error:
            return f"❌ Error: {resp.error.message}", no_update, no_update

        return "❌ Credenciales incorrectas", no_update, no_update

    # --- REGISTRO ---
    @app.callback(
        Output("registro-message", "children"),
        Output("input-nombre", "value"),
        Output("input-email-registro", "value"),
        Output("input-password-registro", "value"),
        Output("input-confirm-password", "value"),
        Output("select-rol", "value"),
        Input("btn-crear-usuario", "n_clicks"),
        State("input-nombre", "value"),
        State("input-email-registro", "value"),
        State("input-password-registro", "value"),
        State("input-confirm-password", "value"),
        State("select-rol", "value"),
        prevent_initial_call=True
    )
    def registrar(n, nombre, email, password, confirm, rol):
        if not all([nombre, email, password, confirm]):
            return "⚠️ Complete todos los campos", no_update, no_update, no_update, no_update, no_update

        if password != confirm:
            return "⚠️ Las contraseñas no coinciden", no_update, no_update, no_update, no_update, no_update

        if usuario_model.evaluar_password_strength(password) < 50:
            return "⚠️ La contraseña es demasiado débil", no_update, no_update, no_update, no_update, no_update

        resp = usuario_model.crear_usuario(nombre, email, password, rol)

        if resp.user:
            return (
                "✅ Usuario creado con éxito",
                "",  # limpiar nombre
                "",  # limpiar email
                "",  # limpiar password
                "",  # limpiar confirm
                "cliente"  # reset rol
            )

        if resp.error:
            return f"❌ Error: {resp.error.message}", no_update, no_update, no_update, no_update, no_update

        return "❌ No se pudo crear el usuario", no_update, no_update, no_update, no_update, no_update

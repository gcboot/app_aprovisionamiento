from src.core.db import supabase
import re


def login_usuario(email, password):
    """Autentica usuario en Supabase Auth y devuelve AuthResponse"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        # Retornamos directamente el objeto AuthResponse
        return response
    except Exception as e:
        # Si ocurre un error en la conexión o request
        class ErrorResponse:
            user = None
            session = None
            error = e
        return ErrorResponse()


def crear_usuario(nombre, email, password, rol="cliente"):
    """Registra usuario en Supabase Auth y en la tabla usuarios"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        # Si se creó el usuario, lo registramos en la tabla 'usuarios'
        if response.user:
            supabase.table("usuarios").insert({
                "auth_id": response.user.id,
                "nombre": nombre,
                "rol": rol,
                "correo": email
            }).execute()

        # Retornamos AuthResponse
        return response
    except Exception as e:
        # Mismo truco: devolvemos un objeto con error
        class ErrorResponse:
            user = None
            session = None
            error = e
        return ErrorResponse()


def evaluar_password_strength(password: str) -> int:
    """
    Evalúa la fuerza de una contraseña y devuelve un valor entre 0-100
    (para usar en dmc.Progress).
    """
    score = 0
    if not password:
        return score

    # Longitud
    if len(password) >= 8:
        score += 25
    if len(password) >= 12:
        score += 25

    # Letras mayúsculas y minúsculas
    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 20

    # Números
    if re.search(r"\d", password):
        score += 15

    # Caracteres especiales
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 15

    return min(score, 100)

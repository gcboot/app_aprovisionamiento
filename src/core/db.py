# src/core/db.py
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Autenticación con Supabase Auth ---
def autenticar_usuario(correo: str, contrasena: str):
    """Autentica contra Supabase Auth y devuelve datos básicos"""
    return supabase.auth.sign_in_with_password({
        "email": correo,
        "password": contrasena
    })

# --- Obtener datos extendidos del usuario ---
def obtener_usuario_por_auth_id(auth_id: str):
    """Busca en la tabla usuarios el rol, nombre, etc. usando el auth_id"""
    return supabase.table("usuarios").select("*").eq("auth_id", auth_id).execute()

# --- Registrar sesión ---
def crear_sesion(usuario_id: str, ip: str, dispositivo: str):
    """Inserta nueva sesión"""
    return supabase.table("sesiones").insert({
        "usuario_id": usuario_id,
        "ip": ip,
        "dispositivos": dispositivo,
        "activo": True
    }).execute()


# --- Cerrar sesión ---
def cerrar_sesion(sesion_id: int):
    """Finaliza la sesión actualizando fin y activo=False"""
    return supabase.table("sesiones").update({
        "fin": datetime.utcnow().isoformat(),
        "activo": False
    }).eq("id", sesion_id).execute()

# --- Cerrar sesión global en Supabase Auth (opcional) ---
def cerrar_sesion_auth():
    """Cierra sesión en Supabase Auth (JWT)"""
    return supabase.auth.sign_out()
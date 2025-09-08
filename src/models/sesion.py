from src.core.db import supabase

def guardar_sesion(auth_id, rol_default="cliente"):
    """
    Crea un objeto de sesión que se guarda en dcc.Store.
    Incluye datos del usuario desde la tabla usuarios.
    """
    try:
        # Buscar usuario en la tabla 'usuarios'
        resp = supabase.table("usuarios").select("id, nombre, rol, correo").eq("auth_id", auth_id).single().execute()

        if resp.data:
            return {
                "id": resp.data["id"],
                "auth_id": auth_id,
                "nombre": resp.data.get("nombre"),
                "rol": resp.data.get("rol", rol_default),
                "correo": resp.data.get("correo")
            }
    except Exception as e:
        print("❌ Error al cargar sesión:", e)

    # fallback mínimo si no encuentra en la BD
    return {"auth_id": auth_id, "rol": rol_default}


def cerrar_sesion():
    """
    Limpia la sesión (para logout).
    """
    return None

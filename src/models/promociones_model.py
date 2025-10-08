from src.core.db import supabase

TABLA = "promociones"


def get_all_promociones():
    """Obtiene todas las promociones."""
    query = supabase.table(TABLA).select("*").execute()
    return query.data


def get_promocion(id_promocion: str):
    """Obtiene una promoción por su ID."""
    query = supabase.table(TABLA).select("*").eq("id", id_promocion).single().execute()
    return query.data


def crear_promocion(nombre: str, tipo: str, codigo_padre: int = None, id_campania: str = None):
    """Crea una promoción nueva."""
    data = {"nombre": nombre, "tipo": tipo, "codigo_padre": codigo_padre, "id_campania": id_campania}
    query = supabase.table(TABLA).insert(data).execute()
    return query.data


def actualizar_promocion(id_promocion: str, updates: dict):
    """Actualiza una promoción existente."""
    query = supabase.table(TABLA).update(updates).eq("id", id_promocion).execute()
    return query.data


def eliminar_promocion(id_promocion: str):
    """Elimina una promoción por ID."""
    query = supabase.table(TABLA).delete().eq("id", id_promocion).execute()
    return query.data

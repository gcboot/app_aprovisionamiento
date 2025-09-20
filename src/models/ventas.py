from src.core.db import supabase


# ---------- Procesar staging ----------
def procesar_staging():
    """
    Llama a la función procesar_staging() en Supabase.
    Retorna resumen de inserciones.
    """
    res = supabase.rpc("procesar_staging").execute()
    if res.data:
        return res.data[0]  # Supabase devuelve lista de resultados
    return {"ventas_insertadas": 0, "eventos_insertados": 0}


# ---------- Obtener ventas ----------
def get_ventas(filtros: dict = None):
    """
    Retorna ventas con opción de filtros.
    filtros: {"pais": "GT", "id_campania": 12, "codigo": "4117273718"}
    """
    query = supabase.table("ventas").select("*, productos(nombre), campanias(anio, campania)")

    if filtros:
        for k, v in filtros.items():
            if v:
                query = query.eq(k, v)

    res = query.limit(200).execute()
    return res.data


# ---------- Obtener eventos ----------
def get_eventos(filtros: dict = None):
    """
    Retorna eventos de venta con opción de filtros.
    filtros: {"tipo_evento": "agotado_web", "id_campania": 12}
    """
    query = supabase.table("eventos_venta").select("*")

    if filtros:
        for k, v in filtros.items():
            if v:
                query = query.eq(k, v)

    res = query.limit(200).execute()
    return res.data

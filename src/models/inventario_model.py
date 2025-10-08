from src.core.db import supabase

def get_inventario():
    result = supabase.table("inventario").select(
        "id, codigo, stock_inicial, stock_actual, stock_minimo, stock_reservado, fecha"
    ).execute()
    return result.data

def insert_inventario(codigo, stock_inicial, stock_actual, stock_minimo, stock_reservado, fecha, actualizado_por=None):
    result = supabase.table("inventario").insert({
        "codigo": codigo,
        "stock_inicial": stock_inicial,
        "stock_actual": stock_actual,
        "stock_minimo": stock_minimo,
        "stock_reservado": stock_reservado,
        "fecha": fecha,
        "actualizado_por": actualizado_por
    }).execute()
    return result.data[0]["id"] if result.data else None

def update_inventario(id, stock_inicial, stock_actual, stock_minimo, stock_reservado, fecha, actualizado_por=None):
    supabase.table("inventario").update({
        "stock_inicial": stock_inicial,
        "stock_actual": stock_actual,
        "stock_minimo": stock_minimo,
        "stock_reservado": stock_reservado,
        "fecha": fecha,
        "actualizado_por": actualizado_por
    }).eq("id", id).execute()

def delete_inventario(id):
    supabase.table("inventario").delete().eq("id", id).execute()

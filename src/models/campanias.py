from src.core.db import supabase

def get_campanias():
    result = supabase.table('campanias').select(
        'id, campania, anio, fecha_inicio, fecha_fin, estado'
    ).execute()
    return result.data

def insert_campania(campania, anio, fecha_inicio, fecha_fin, estado='programada'):
    supabase.table('campanias').insert({
        'campania': campania,
        'anio': anio,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'estado': estado
    }).execute()

def update_campania(id, campania, anio, fecha_inicio, fecha_fin, estado):
    supabase.table("campanias").update({
        "campania": campania,
        "anio": anio,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "estado": estado
    }).eq("id", id).execute()

def delete_campania(id):
    supabase.table('campanias').delete().eq('id', id).execute()

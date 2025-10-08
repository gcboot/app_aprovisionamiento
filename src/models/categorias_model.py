from src.core.db import supabase

def get_categorias():
    result = supabase.table("categorias").select("id, nombre, descripcion").execute()
    return result.data

def insert_categoria(nombre, descripcion):
    supabase.table("categorias").insert({
        "nombre": nombre,
        "descripcion": descripcion
    }).execute()

def update_categoria(id, nombre, descripcion):
    supabase.table("categorias").update({
        "nombre": nombre,
        "descripcion": descripcion,
        "actualizado_en": "now()"
    }).eq("id", id).execute()

def delete_categoria(id):
    supabase.table("categorias").delete().eq("id", id).execute()

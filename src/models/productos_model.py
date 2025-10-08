from src.core.db import supabase

def get_productos():
    result = supabase.table('productos').select(
        'id, codigo, nombre, precio_base, es_original, id_categoria'
    ).execute()
    return result.data

def get_productos_originales():
    result = supabase.table('productos').select(
        'id, codigo, nombre'
    ).eq('es_original', True).execute()
    return result.data

def insert_producto(codigo, nombre, precio_base, es_original, id_categoria):
    result = supabase.table('productos').insert({
        'codigo': codigo,
        'nombre': nombre,
        'precio_base': precio_base,
        'es_original': es_original,
        'id_categoria': id_categoria
    }).execute()
    return result.data[0]["id"] if result.data else None

def update_producto(id, codigo, nombre, precio_base, es_original, id_categoria):
    supabase.table("productos").update({
        "codigo": codigo,
        "nombre": nombre,
        "precio_base": precio_base,
        "es_original": es_original,
        "id_categoria": id_categoria
    }).eq("id", id).execute()

def delete_producto(id):
    supabase.table('productos').delete().eq('id', id).execute()

# --- Relaciones producto_oferta ---
def insert_producto_oferta(id_oferta, id_original):
    supabase.table('producto_oferta').insert({
        "id_oferta": id_oferta,
        "id_original": id_original
    }).execute()

def get_producto_original(id_oferta):
    result = supabase.table('producto_oferta').select(
        'id_original'
    ).eq('id_oferta', id_oferta).execute()
    return result.data

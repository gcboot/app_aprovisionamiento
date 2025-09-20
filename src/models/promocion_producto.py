# from src.core.db import supabase

# TABLA = "promocion_producto"


# def get_all_promocion_producto():
#     """Obtiene todos los registros de la tabla promocion_producto."""
#     query = (
#         supabase.table(TABLA)
#         .select("id_promocion, codigo, cantidad, promociones(nombre, tipo), productos(nombre)")
#         .execute()
#     )
#     return query.data


# def get_promocion_producto(id_promocion: str, codigo: int):
#     """Obtiene un registro específico por llave compuesta."""
#     query = (
#         supabase.table(TABLA)
#         .select("*")
#         .eq("id_promocion", id_promocion)
#         .eq("codigo", codigo)
#         .single()
#         .execute()
#     )
#     return query.data


# def crear_promocion_producto(id_promocion: str, codigo: int, cantidad: int = 1):
#     """Crea un nuevo registro en promocion_producto."""
#     data = {"id_promocion": id_promocion, "codigo": codigo, "cantidad": cantidad}
#     query = supabase.table(TABLA).insert(data).execute()
#     return query.data


# def actualizar_promocion_producto(id_promocion: str, codigo: int, cantidad: int):
#     """Actualiza la cantidad de un producto en una promoción."""
#     query = (
#         supabase.table(TABLA)
#         .update({"cantidad": cantidad})
#         .eq("id_promocion", id_promocion)
#         .eq("codigo", codigo)
#         .execute()
#     )
#     return query.data


# def eliminar_promocion_producto(id_promocion: str, codigo: int):
#     """Elimina un producto dentro de una promoción."""
#     query = (
#         supabase.table(TABLA)
#         .delete()
#         .eq("id_promocion", id_promocion)
#         .eq("codigo", codigo)
#         .execute()
#     )
#     return query.data

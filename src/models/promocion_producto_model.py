from src.core.db import supabase

def get_promocion_productos():
    """
    Devuelve todas las relaciones promoción–producto,
    incluyendo datos de la promoción y del producto.
    """
    try:
        response = (
            supabase.table("promocion_producto")
            .select(
                """
                id_promocion,
                codigo,
                cantidad,
                promociones!promocion_producto_id_promocion_fkey (id, nombre, tipo, id_campania),
                productos!promocion_producto_codigo_fkey (codigo, nombre, precio_base)
                """
            )
            .order("id_promocion", desc=False)
            .execute()
        )
        data = response.data or []
        registros = []

        for r in data:
            registros.append({
                "id_promocion": r["id_promocion"],
                "codigo": r["codigo"],
                "cantidad": r["cantidad"],
                "promocion": (
                    r.get("promociones", {}).get("nombre")
                    if r.get("promociones") else None
                ),
                "tipo": (
                    r.get("promociones", {}).get("tipo")
                    if r.get("promociones") else None
                ),
                "id_campania": (
                    r.get("promociones", {}).get("id_campania")
                    if r.get("promociones") else None
                ),
                "producto": (
                    r.get("productos", {}).get("nombre")
                    if r.get("productos") else None
                ),
                "precio_base": (
                    r.get("productos", {}).get("precio_base")
                    if r.get("productos") else None
                ),
            })

        return registros
    except Exception as e:
        print("❌ Error en get_promocion_productos:", e)
        return []


def get_promocion_producto(id_promocion, codigo):
    """
    Devuelve un único registro promoción–producto.
    """
    try:
        response = (
            supabase.table("promocion_producto")
            .select(
                """
                id_promocion,
                codigo,
                cantidad,
                promociones!promocion_producto_id_promocion_fkey (id, nombre, tipo, id_campania),
                productos!promocion_producto_codigo_fkey (codigo, nombre, precio_base)
                """
            )
            .eq("id_promocion", id_promocion)
            .eq("codigo", codigo)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None
    except Exception as e:
        print("❌ Error en get_promocion_producto:", e)
        return None


def insert_promocion_producto(id_promocion, codigo, cantidad=1):
    """Inserta un nuevo registro promoción–producto."""
    try:
        response = (
            supabase.table("promocion_producto")
            .insert({
                "id_promocion": id_promocion,
                "codigo": int(codigo),
                "cantidad": int(cantidad),
            })
            .execute()
        )
        print("✅ Insert promocion_producto:", response)
        return response.data
    except Exception as e:
        print("❌ Error en insert_promocion_producto:", e)
        return None


def update_promocion_producto(id_promocion, codigo, cantidad):
    """Actualiza la cantidad de un registro promoción–producto existente."""
    try:
        response = (
            supabase.table("promocion_producto")
            .update({"cantidad": int(cantidad)})
            .eq("id_promocion", id_promocion)
            .eq("codigo", int(codigo))
            .execute()
        )
        print("✅ Update promocion_producto:", response)
        return response.data
    except Exception as e:
        print("❌ Error en update_promocion_producto:", e)
        return None


def delete_promocion_producto(id_promocion, codigo):
    """Elimina un registro promoción–producto."""
    try:
        response = (
            supabase.table("promocion_producto")
            .delete()
            .eq("id_promocion", id_promocion)
            .eq("codigo", int(codigo))
            .execute()
        )
        print("🗑 Delete promocion_producto:", response)
        return response.data
    except Exception as e:
        print("❌ Error en delete_promocion_producto:", e)
        return None

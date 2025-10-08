from src.core.db import supabase

def get_all_producto_campania():
    """
    Devuelve todos los registros de producto_campania con datos relacionados
    de productos y campañas.
    """
    try:
        response = supabase.table("producto_campania").select(
            "codigo, precio_oferta, productos(nombre), campanias(campania, anio)"
        ).execute()
        data = response.data or []
        registros = []

        for r in data:
            registros.append({
                "codigo": r["codigo"],
                "producto": r.get("productos", {}).get("nombre") if r.get("productos") else None,
                "campania": r.get("campanias", {}).get("campania") if r.get("campanias") else None,
                "anio": r.get("campanias", {}).get("anio") if r.get("campanias") else None,
                "precio_oferta": r["precio_oferta"]
            })

        return registros
    except Exception as e:
        print("❌ Error en get_all_producto_campania:", e)
        return []


def insert_producto_campania(codigo: int, id_campania: str, precio_oferta: float):
    """
    Inserta un nuevo producto en campaña.
    - codigo: int (producto)
    - id_campania: str (UUID de la campaña)
    - precio_oferta: float
    """
    try:
        response = supabase.table("producto_campania").insert({
            "codigo": int(codigo),
            "id_campania": id_campania,   # UUID como string
            "precio_oferta": float(precio_oferta)
        }).execute()
        print("✅ Insert producto_campania:", response)
        return response.data
    except Exception as e:
        print("❌ Error en insert_producto_campania:", e)
        return None


def update_producto_campania(codigo: int, id_campania: str, precio_oferta: float):
    """
    Actualiza el precio de un producto en campaña.
    """
    try:
        response = supabase.table("producto_campania").update({
            "precio_oferta": float(precio_oferta)
        }).eq("codigo", int(codigo)).eq("id_campania", id_campania).execute()
        print("✅ Update producto_campania:", response)
        return response.data
    except Exception as e:
        print("❌ Error en update_producto_campania:", e)
        return None


def delete_producto_campania(codigo: int, id_campania: str):
    """
    Elimina un producto asignado a una campaña.
    """
    try:
        response = supabase.table("producto_campania").delete() \
            .eq("codigo", int(codigo)) \
            .eq("id_campania", id_campania) \
            .execute()
        print("🗑 Delete producto_campania:", response)
        return response.data
    except Exception as e:
        print("❌ Error en delete_producto_campania:", e)
        return None

import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from src.core.db import supabase

def test_get_usuarios():
    try:
        response = supabase.table("usuarios").select("*").execute()
        print("✅ Conexión exitosa")
        print("📋 Datos devueltos:", response.data)
        assert response.data is not None
    except Exception as e:
        print("Error al traer usuarios:", e)
        raise

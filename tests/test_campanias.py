import pytest
from src.models import campanias
from src.core.db import supabase


# 🔹 Fixture: limpiar tabla antes de cada test
@pytest.fixture(autouse=True)
def limpiar_campanias():
    # Borra todas las campañas antes de cada test
    supabase.table("campanias").delete().neq(
        "id", "00000000-0000-0000-0000-000000000000"
    ).execute()


# 🔹 Test insertar y consultar campañas
def test_insert_and_get_campanias():
    campanias.insert_campania(1, 2025, "2025-01-01", "2025-01-31", "cerrada")
    lista = campanias.get_campanias()
    assert any(c["campania"] == 1 and c["anio"] == 2025 for c in lista)


# 🔹 Test actualizar campaña
def test_update_campania():
    campanias.insert_campania(2, 2025, "2025-02-01", "2025-02-28", "programada")
    lista = campanias.get_campanias()
    camp_id = next(c["id"] for c in lista if c["campania"] == 2 and c["anio"] == 2025)

    campanias.update_campania(camp_id, 2, 2025, "2025-02-01", "2025-02-28", "activa")
    lista2 = campanias.get_campanias()
    camp2 = next(c for c in lista2 if c["id"] == camp_id)

    assert camp2["estado"] == "activa"


# 🔹 Test eliminar campaña
def test_delete_campania():
    campanias.insert_campania(3, 2025, "2025-03-01", "2025-03-31", "programada")
    lista = campanias.get_campanias()
    camp = next(c for c in lista if c["campania"] == 3 and c["anio"] == 2025)

    campanias.delete_campania(camp["id"])
    lista2 = campanias.get_campanias()

    assert all(c["id"] != camp["id"] for c in lista2)

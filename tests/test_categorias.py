import pytest
from models import categorias_model
from src.core.db import supabase


# 🔹 Fixture: limpiar tabla antes de cada test
@pytest.fixture(autouse=True)
def limpiar_categorias():
    supabase.table("categorias").delete().neq("id", 0).execute()
    # Nota: .neq("id", 0) es un truco porque supabase no permite delete() sin filtro.
    # Básicamente borra todos los registros ya que no habrá id = 0.


# 🔹 Test insertar y consultar
def test_insert_and_get_categorias():
    categorias_model.insert_categoria("Electrónica", "Dispositivos electrónicos")
    lista = categorias_model.get_categorias()
    assert any(cat["nombre"] == "Electrónica" for cat in lista)


# 🔹 Test actualizar
def test_update_categoria():
    categorias_model.insert_categoria("Temporal", "Para Actualizar")
    lista = categorias_model.get_categorias()
    cat_id = next(cat["id"] for cat in lista if cat["nombre"] == "Temporal")

    categorias_model.update_categoria(cat_id, "Temporal Actualizada", "Cambiado")
    lista2 = categorias_model.get_categorias()
    cat2 = next(cat for cat in lista2 if cat["id"] == cat_id)

    assert cat2["nombre"] == "Temporal Actualizada"
    assert cat2["descripcion"] == "Cambiado"


# 🔹 Test eliminar
def test_delete_categoria():
    categorias_model.insert_categoria("Eliminar", "Temporal")
    lista = categorias_model.get_categorias()
    cat = next(c for c in lista if c["nombre"] == "Eliminar")

    categorias_model.delete_categoria(cat["id"])
    lista2 = categorias_model.get_categorias()

    assert all(c["id"] != cat["id"] for c in lista2)

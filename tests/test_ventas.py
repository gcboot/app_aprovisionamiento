import pytest
import uuid
from src.models import ventas

# UUID de campaña dummy (ya cargado en tabla campanias)
CAMPANIA_TEST_UUID = "11111111-1111-1111-1111-111111111113"
CODIGO_PRODUCTO_TEST = 9000000002  # producto dummy en tabla productos

# ---------- Test de conexión ----------
def test_conexion_supabase():
    registros = ventas.get_all_ventas()
    assert registros is not None, "❌ No se pudo conectar a ventas"
    assert isinstance(registros, list), "❌ El resultado debería ser una lista"

# ---------- Test de inserción ----------
def test_crear_venta():
    codigo_unico = f"VENTA_TEST_{uuid.uuid4().hex[:6]}"
    nueva = {
        "codigo_venta": codigo_unico,
        "codigo": CODIGO_PRODUCTO_TEST,
        "id_campania": CAMPANIA_TEST_UUID,
        "pais": "HN",
        "fecha": "2025-09-20",
        "unidades": 11,
        "precio_unitario": 33.33,
        "valor_q": 333.00,
    }

    resultado = ventas.crear_venta(nueva)

    assert resultado is not None, "❌ La inserción falló"
    assert resultado["codigo_venta"] == codigo_unico
    assert resultado["unidades"] == 11
    assert resultado["valor_q"] == 333.00

# ---------- Test de consultas ----------
def test_get_ventas_filtradas():
    registros = ventas.get_ventas_por_campania(CAMPANIA_TEST_UUID, pais="GT")
    assert isinstance(registros, list)
    if registros:
        assert "codigo_venta" in registros[0]
        assert "unidades" in registros[0]

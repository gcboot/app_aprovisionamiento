import pandas as pd
from io import StringIO
from src.core.db import supabase

# ---------- Insertar CSV al staging ----------
def cargar_csv_ventas(file_content: str):
    """
    Recibe contenido CSV (como string), lo carga en ventas_raw.
    Retorna DataFrame de preview (primeras filas).
    """

    # Leer CSV en DataFrame
    df = pd.read_csv(StringIO(file_content))

    # Validar columnas mínimas esperadas
    columnas_requeridas = [
        "pais", "anio", "campania", "producto", "codigo_original",
        "demanda_parcial_unidades", "demanda_parcial_q",
        "agotados_web_unidades", "agotados_web_q",
        "pedidos_bloqueados_unidades", "pedidos_bloqueados_q"
    ]
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"Falta la columna obligatoria en CSV: {col}")

    # Convertir a lista de dicts para insertar
    records = df.to_dict(orient="records")

    # Insertar en bloque (más eficiente que fila por fila)
    if records:
        supabase.table("ventas_raw").insert(records).execute()

    return df.head(10)  # devolver preview


def get_staging(limit: int = 100):
    """
    Obtiene registros en staging (ventas_raw).
    """
    res = supabase.table("ventas_raw").select("*").limit(limit).execute()
    return res.data


def limpiar_staging():
    """
    Borra todo el staging (para reiniciar carga).
    """
    supabase.table("ventas_raw").delete().neq("id_raw", 0).execute()

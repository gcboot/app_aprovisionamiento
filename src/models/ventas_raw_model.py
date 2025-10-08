import pandas as pd
from io import StringIO
import unicodedata
from postgrest.exceptions import APIError
from src.core.db import supabase

# ---------- Insertar CSV al staging ----------
def cargar_csv_ventas(file_content: str, supabase=None):
    """
    Recibe contenido CSV (como string) y lo carga en la tabla ventas_raw de Supabase.
    Retorna un dict con:
      - ok: bool → indica éxito o error
      - mensaje: str → texto descriptivo para mostrar al usuario
      - preview: DataFrame o None → primeras filas del archivo cargado
    """
    try:
        # 1️⃣ Leer CSV en DataFrame
        df = pd.read_csv(StringIO(file_content))

        # 2️⃣ Validar columnas
        validacion = validar_columnas(df)
        if not validacion["ok"]:
            return {
                "ok": False,
                "mensaje": validacion["mensaje"],
                "preview": None
            }

        # 3️⃣ Intentar insertar en Supabase
        if supabase is not None:
            try:
                data = df.to_dict(orient="records")
                supabase.table("ventas_raw").insert(data).execute()
            except APIError as e:
                msg = e.args[0].get("message", "")
                if "Could not find the" in msg and "column" in msg:
                    col = msg.split("'")[1]
                    return {
                        "ok": False,
                        "mensaje": (
                            f"❌ Columna inválida: '{col}' no existe en la base de datos.\n"
                            f"👉 Revisa tu CSV: usa 'anio' en lugar de '{col}' si contiene una ñ."
                        ),
                        "preview": None
                    }
                else:
                    return {
                        "ok": False,
                        "mensaje": f"⚠️ Error al insertar en la base de datos: {msg}",
                        "preview": None
                    }

        # 4️⃣ Retornar éxito y preview (como DataFrame real)
        return {
            "ok": True,
            "mensaje": "✅ CSV cargado correctamente en ventas_raw.",
            "preview": df.head(5)
        }

    except Exception as e:
        return {
            "ok": False,
            "mensaje": f"⚠️ Error cargando CSV: {str(e)}",
            "preview": None
        }

    # Validar columnas mínimas esperadas

def normalizar_columna(col):
    """
    Normaliza un nombre de columna:
    - Convierte a minúsculas
    - Elimina tildes/acentos
    """
    return ''.join(
        c for c in unicodedata.normalize('NFKD', col.lower())
        if not unicodedata.combining(c)
    )

def validar_columnas(df):
    """
    Valida que el DataFrame tenga todas las columnas requeridas.
    Devuelve dict con estado y mensaje en lugar de romper el flujo.
    """
    if df is None:
        return {
            "ok": False,
            "mensaje": "❌ No se pudo cargar el archivo, el DataFrame está vacío."
        }

    columnas_requeridas = [
        "pais", "anio", "campania", "producto", "codigo_original",
        "demanda_parcial_unidades", "demanda_parcial_q",
        "agotados_web_unidades", "agotados_web_q",
        "pedidos_bloqueados_unidades", "pedidos_bloqueados_q"
    ]

    # Normalizar nombres de columnas en DataFrame
    columnas_df = [normalizar_columna(c) for c in df.columns]
    faltantes = [col for col in columnas_requeridas if col not in columnas_df]

    if faltantes:
        return {
            "ok": False,
            "mensaje": f"❌ Error: faltan columnas obligatorias o con formato incorrecto: {', '.join(faltantes)}"
        }

    return {
        "ok": True,
        "mensaje": "✅ Todas las columnas requeridas están presentes."
    }
    

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

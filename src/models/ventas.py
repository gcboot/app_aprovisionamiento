from src.core.db import supabase
import uuid

# ----------------- Utilidad -----------------
def normalizar_pais(pais: str) -> str:
    mapping = {
        "GUATEMALA": "GT", "GT": "GT",
        "HONDURAS": "HN", "HN": "HN",
        "EL SALVADOR": "SV", "SV": "SV",
        "NICARAGUA": "NI", "NI": "NI",
        "COSTA RICA": "CR", "CR": "CR",
        "PANAMA": "PA", "PA": "PA",
        "REP. DOMINICANA": "DO", "DO": "DO",
    }
    return mapping.get(pais.strip().upper(), pais.strip().upper())

# ----------------- ETL: procesar staging -----------------
def procesar_staging():
    resp = supabase.table("ventas_raw").select("*").execute()
    if not resp.data:
        return {
            "ventas_insertadas": 0,
            "eventos_insertados": 0,
            "mensaje": "No hay datos en staging."
        }
    registros_staging = resp.data

    # Campañas existentes
    camp_resp = supabase.table("campanias").select("id, anio, campania, fecha_inicio").execute()
    campañas = {(c["anio"], c["campania"]): c for c in camp_resp.data}

    # Precios producto_campania
    pc_resp = supabase.table("producto_campania").select("codigo, id_campania, precio_oferta").execute()
    precios = {(p["codigo"], p["id_campania"]): p["precio_oferta"] for p in pc_resp.data}

    registros_final = []
    for r in registros_staging:
        camp = campañas.get((int(r["anio"]), int(r["campania"])))
        id_camp = camp["id"] if camp else None
        fecha = camp["fecha_inicio"] if camp else None

        precio_unit = precios.get((r["producto"], id_camp), 0.00)
        unidades = r["demanda_parcial_unidades"]

        registros_final.append({
            "codigo_venta": f"STG-{uuid.uuid4().hex[:8]}",
            "codigo": r["producto"],
            "id_campania": id_camp,
            "pais": normalizar_pais(r["pais"]),
            "fecha": fecha,
            "unidades": unidades,
            "precio_unitario": precio_unit,
            "valor_q": precio_unit * unidades,
        })

    resultado = supabase.table("ventas").insert(registros_final).execute()

    # Limpiar staging
    supabase.table("ventas_raw").delete().neq("pais", "").execute()

    return {
        "ventas_insertadas": len(resultado.data) if resultado.data else 0,
        "eventos_insertados": 0,
        "mensaje": f"✅ Se procesaron {len(resultado.data) if resultado.data else 0} registros desde staging."
    }

# ----------------- CRUD Ventas -----------------
def get_all_ventas():
    """
    Obtiene un resumen de ventas agrupado por país y campaña.
    """
    resp = (
        supabase.table("ventas")
        .select("pais, unidades, valor_q, campanias(campania, anio)")
        .execute()
    )
    registros = resp.data or []

    # Agrupación manual en Python
    agrupado = {}
    for r in registros:
        if "campanias" in r and r["campanias"]:
            num = int(r['campanias']['campania'])
            campania_legible = f"C{num:02d}-{r['campanias']['anio']}"
        else:
            campania_legible = "N/A"

        clave = (r["pais"], campania_legible)

        if clave not in agrupado:
            agrupado[clave] = {
                "pais": r["pais"],
                "campania_legible": campania_legible,
                "unidades": 0,
                "valor_q": 0.0
            }

        agrupado[clave]["unidades"] += r.get("unidades", 0)
        agrupado[clave]["valor_q"] += r.get("valor_q", 0.0)

    return list(agrupado.values())

def get_ventas_por_campania(id_campania: str, pais: str = None):
    """
    Obtiene ventas filtradas por campaña (y país si se pasa).
    """
    query = supabase.table("ventas").select(
        "pais, unidades, valor_q, campanias(campania, anio)"
    ).eq("id_campania", id_campania)
    if pais:
        query = query.eq("pais", pais)
    resp = query.execute()
    registros = resp.data or []

    # Agrupación manual
    agrupado = {}
    for r in registros:
        if "campanias" in r and r["campanias"]:
            num = int(r['campanias']['campania'])
            campania_legible = f"C{num:02d}-{r['campanias']['anio']}"
        else:
            campania_legible = "N/A"

        clave = (r["pais"], campania_legible)

        if clave not in agrupado:
            agrupado[clave] = {
                "pais": r["pais"],
                "campania_legible": campania_legible,
                "unidades": 0,
                "valor_q": 0.0
            }

        agrupado[clave]["unidades"] += r.get("unidades", 0)
        agrupado[clave]["valor_q"] += r.get("valor_q", 0.0)

    return list(agrupado.values())

def crear_venta(data: dict):
    """
    Inserta una venta manualmente en la tabla ventas.
    """
    res = supabase.table("ventas").insert(data).execute()
    return res.data[0] if res.data else None

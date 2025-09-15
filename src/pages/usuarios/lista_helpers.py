import dash_mantine_components as dmc
from dash import html
from src.core.db import supabase

def get_usuarios():
    try:
        response = supabase.table("usuarios").select("*").execute()
        return response.data or []
    except Exception as e:
        print("❌ Error al traer usuarios:", e)
        return []

def actualizar_usuario(user_id, nuevo_correo, nuevo_rol):
    try:
        supabase.table("usuarios").update({
            "correo": nuevo_correo,
            "rol": nuevo_rol
        }).eq("id", user_id).execute()
        return True
    except Exception as e:
        print("❌ Error al actualizar:", e)
        return False

def eliminar_usuario(user_id):
    try:
        supabase.table("usuarios").delete().eq("id", user_id).execute()
        return True
    except Exception as e:
        print("❌ Error al eliminar:", e)
        return False

def make_table(usuarios):
    if not usuarios:
        return dmc.Text("⚠️ No hay usuarios registrados", c="red", ta="center")

    return dmc.Table(
        striped=True,
        highlightOnHover=True,
        withTableBorder=True,
        withColumnBorders=True,
        withRowBorders=True,
        children=[
            dmc.TableThead(
                dmc.TableTr([
                    dmc.TableTh("Nombre"),
                    dmc.TableTh("Correo"),
                    dmc.TableTh("Rol"),
                    dmc.TableTh("Acciones"),
                ])
            ),
            dmc.TableTbody([
                dmc.TableTr([
                    dmc.TableTd(user.get("nombre", "—")),
                    dmc.TableTd(user.get("correo") or "—"),
                    dmc.TableTd(user.get("rol", "—")),
                    dmc.TableTd(
                        html.Div([
                            dmc.Button(
                                "Editar",
                                id={"type": "btn-editar", "index": user["id"]},
                                size="xs",
                                color="blue",
                                variant="outline",
                                style={"marginRight": "5px"}
                            ),
                            dmc.Button(
                                "Eliminar",
                                id={"type": "btn-eliminar", "index": user["id"]},
                                size="xs",
                                color="red",
                                variant="outline"
                            )
                        ])
                    )
                ]) for user in usuarios
            ])
        ]
    )

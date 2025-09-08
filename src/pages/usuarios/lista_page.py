import dash
from dash import html, dcc
import dash_mantine_components as dmc
from src.components.layout_base import layout_base
from src.core.db import supabase
from dash_iconify import DashIconify

dash.register_page(
    __name__,
    path="/home/usuarios/lista",
    title="Lista de Usuarios"
)

# --- Helpers ---
def get_usuarios():
    try:
        response = supabase.table("usuarios").select("*").execute()
        print("📋 Usuarios desde supabase:", response.data)
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

# --- Tabla dinámica ---
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
                    dmc.TableTd("Acciones…")  # 👈 botones vienen por callback
                ]) for user in usuarios
            ])
        ]
    )

# --- Contenido principal ---
content = dmc.MantineProvider(
    children=html.Div(
        children=[
            dmc.Title("📋 Lista de Usuarios", order=2),
            dmc.Space(h=20),

            dmc.TextInput(
                id="search-usuarios",
                placeholder="Buscar por nombre o correo...",
                leftSection=DashIconify(icon="mdi:magnify"),
                style={"maxWidth": "400px"}
            ),
            dmc.Space(h=20),

            html.Div(id="tabla-usuarios"),

            dmc.Modal(
                id="modal-editar",
                title="Editar Usuario",
                size="lg",
                children=[
                    dmc.TextInput(label="Nombre", id="edit-user-nombre", disabled=True),
                    dmc.Space(h=15),
                    dmc.TextInput(label="Correo", id="edit-user-correo"),
                    dmc.Space(h=15),
                    dmc.Select(
                        label="Rol",
                        id="edit-user-rol",
                        data=[
                            {"label": "Administrador", "value": "admin"},
                            {"label": "Analista", "value": "analista"},
                            {"label": "Gerente", "value": "gerente"},
                            {"label": "Cliente", "value": "cliente"},
                        ]
                    ),
                    dmc.Space(h=20),
                    dmc.Button("Actualizar", id="btn-actualizar-usuario", color="green"),
                    dmc.Space(h=15),
                    dmc.Text("", id="edit-message", ta="center"),
                    dmc.TextInput(id="edit-user-id", style={"display": "none"})
                ]
            ),

            dmc.Space(h=20),
            dcc.Store(id="refresh-store", data="init", storage_type="memory")
        ]
    )
)

layout = layout_base(content)

import sys, os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import dash
from dash import html, Input, Output
import dash_mantine_components as dmc
from src.core.db import supabase

app = dash.Dash(__name__)


def get_usuarios():
    response = supabase.table("usuarios").select("*").execute()
    print("📋 Usuarios desde supabase:", response.data)
    return response.data or []


def make_table(usuarios):
    if not usuarios:
        return dmc.Text("⚠️ No hay usuarios registrados", c="red", ta="center")
    return dmc.Table(
        striped=True,
        highlightOnHover=True,
        children=[
            dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh("Nombre"),
                        dmc.TableTh("Correo"),
                        dmc.TableTh("Rol"),
                    ]
                )
            ),
            dmc.TableTbody(
                [
                    dmc.TableTr(
                        [
                            dmc.TableTd(u.get("nombre", "—")),
                            dmc.TableTd(u.get("correo") or "—"),
                            dmc.TableTd(u.get("rol", "—")),
                        ]
                    )
                    for u in usuarios
                ]
            ),
        ],
    )


app.layout = dmc.MantineProvider(  # 👈 envolvemos la app
    children=html.Div(
        [
            dmc.Title("🔎 Test Lista de Usuarios", order=2),
            html.Button("Refrescar", id="btn-refresh"),
            html.Div(id="tabla"),
        ]
    )
)


@app.callback(
    Output("tabla", "children"),
    Input("btn-refresh", "n_clicks"),
    prevent_initial_call=False,
)
def mostrar_tabla(n):
    usuarios = get_usuarios()
    return make_table(usuarios)


if __name__ == "__main__":
    app.run(debug=True)

import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from src.models import campanias
from src.components.layout_base import layout_base  # tu layout base

# Registrar página
dash.register_page(
    __name__,
    path="/home/promociones",
    name="Promociones"
)


def layout():
    content = dmc.Container([
        # ---------- Título y botón nuevo ----------
        dmc.Group([
            dmc.Title("Promociones", order=2),
            dmc.Button(
                "➕ Nueva Promoción",
                id="btn-nueva-promocion",
                color="blue",
                leftSection=DashIconify(icon="tabler:plus")
            )
        ], justify="space-between", mb=20),

        # ---------- Tabla ----------
        html.Div(id="tabla-promociones"),

        # ---------- Modal Crear/Editar ----------
        dmc.Modal(
            id="modal-promocion",
            title="Gestión de Promoción",
            size="lg",
            centered=True,
            opened=False,   # 👈 siempre inicia cerrado
            children=[
                dmc.TextInput(
                    id="input-nombre-promocion",
                    label="Nombre de la Promoción",
                    placeholder="Ej. Combo Shampoo + Acondicionador",
                    required=True,
                    mb=10,
                    persistence=True
                ),
                dmc.Select(
                    id="select-tipo-promocion",
                    label="Tipo de Promoción",
                    placeholder="Seleccione un tipo",
                    data=[
                        {"label": "Combo", "value": "combo"},
                        {"label": "2x1", "value": "2x1"},
                        {"label": "Descuento", "value": "descuento"},
                        {"label": "Automático", "value": "automatico"}
                    ],
                    required=True,
                    mb=10,
                    persistence=True
                ),
                dmc.NumberInput(
                    id="input-codigo-padre",
                    label="Código Padre (opcional)",
                    placeholder="Ingrese el código del producto principal",
                    min=0,
                    step=1,
                    mb=10,
                    persistence=True
                ),
                dmc.Select(
                    id="select-campania-promocion",
                    label="Campaña",
                    placeholder="Seleccione campaña",
                    data=[{"label": f"C{c['campania']} - {c['anio']}", "value": str(c["id"])}
                          for c in campanias.get_campanias()],
                    required=True,
                    mb=20,
                    persistence=True
                ),

                # Hidden field para edición
                dmc.TextInput(id="hidden-id-promocion", value="", style={"display": "none"}),

                # ---------- Botones ----------
                dmc.Group(
                    [
                        dmc.Button("Cancelar", id="btn-cancelar-promocion", color="red", variant="outline"),
                        dmc.Button("Guardar", id="btn-save-promocion", color="blue"),
                    ],
                    justify="flex-end",
                    align="center"
                )
            ]
        )
    ])

    return layout_base(content)

import dash
from dash import html
import dash_mantine_components as dmc
from src.models import productos, campanias
from src.components.layout_base import layout_base  # tu layout base

# Registrar página con la nueva ruta
dash.register_page(
    __name__,
    path="/home/productos_campania",
    name="Producto_Campaña"
)

def layout():
    content = dmc.Container([
        dmc.Title("Asignar Productos a Campañas", order=2, mb=20),

        dmc.Button("➕ Nuevo Registro", id="btn-open-modal", color="blue", mb=20),

        html.Div(id="tabla-producto-campania"),

        # Modal Crear/Editar
        dmc.Modal(
            id="modal-pc",
            title="Producto-Campaña",
            size="lg",
            centered=True,
            opened=False,   # 👈 siempre arranca cerrado
            children=[
                dmc.Select(
                    id="select-producto",
                    label="Producto",
                    placeholder="Seleccione producto",
                    data=[{"label": f"{p['nombre']} ({p['codigo']})", "value": str(p["codigo"])}
                          for p in productos.get_productos()],
                    mb=10,
                    persistence=True
                ),
                dmc.Select(
                    id="select-campania",
                    label="Campaña",
                    placeholder="Seleccione campaña",
                    data=[{"label": f"C{c['campania']} - {c['anio']}", "value": str(c["id"])}
                          for c in campanias.get_campanias()],
                    mb=10,
                    persistence=True
                ),
                dmc.NumberInput(
                    id="input-precio",
                    label="Precio Oferta",
                    min=0,
                    step=0.01,
                    decimalScale=2,          # controla decimales
                    fixedDecimalScale=True,  # siempre muestra 2
                    allowDecimal=True,       # permite decimales
                    mb=20,
                    persistence=True
                ),
                # Hidden fields para identificar si es edición
                dmc.TextInput(id="hidden-codigo", value="", style={"display": "none"}),
                dmc.TextInput(id="hidden-id-campania", value="", style={"display": "none"}),

                dmc.Group(
                    [
                        dmc.Button("Guardar", id="btn-save-pc", color="blue"),
                        dmc.Button("Cancelar", id="btn-close-modal", color="red", variant="outline"),
                    ],
                    justify="flex-end",
                    align="center"
                )
            ]
        )
    ])

    # Retornar el contenido envuelto en el layout base
    return layout_base(content)

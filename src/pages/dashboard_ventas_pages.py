import dash
from dash import html, dcc
import dash_mantine_components as dmc
import plotly.express as px

from src.models import ventas_model
from src.components.layout_base import layout_base  # tu layout base general

# Registrar página
dash.register_page(
    __name__,
    path="/home/dashboard_ventas",
    name="Dashboard Ventas"
)

def layout():
    # ---------- Datos desde Supabase ----------
    registros = ventas_model.get_all_ventas()
    if not registros:
        return layout_base(
            dmc.Container([
                dmc.Title("📊 Dashboard de Ventas", order=2, mb=20),
                dmc.Alert(
                    "No hay ventas registradas en la base de datos.",
                    color="yellow",
                    variant="filled"
                )
            ])
        )

    # ---------- KPIs ----------
    total_q = sum([r["valor_q"] for r in registros])
    total_unidades = sum([r["unidades"] for r in registros])
    ticket_promedio = total_q / total_unidades if total_unidades > 0 else 0

    # ---------- Gráficas ----------
    # Ventas por campaña
    df_campania = {}
    for r in registros:
        clave = r.get("campania_legible", "N/A")
        df_campania[clave] = df_campania.get(clave, 0) + r["valor_q"]

    fig_campania = px.bar(
        x=list(df_campania.keys()),
        y=list(df_campania.values()),
        labels={"x": "Campaña", "y": "Ventas (Q)"},
        title="Ventas por campaña"
    )

    # Ventas por país
    df_pais = {}
    for r in registros:
        df_pais[r["pais"]] = df_pais.get(r["pais"], 0) + r["valor_q"]

    fig_pais = px.pie(
        values=list(df_pais.values()),
        names=list(df_pais.keys()),
        title="Distribución de ventas por país"
    )

    # ---------- Contenido ----------
    contenido = dmc.Container([

        dmc.Title("📊 Dashboard de Ventas", order=2, mb=20),

        # KPIs
        dmc.Grid([
            dmc.GridCol(
                dmc.Paper(dmc.Stack([
                    dmc.Text("Total Ventas (Q)", size="sm", fw=500),
                    dmc.Text(f"Q{total_q:,.2f}", size="xl", fw=700)
                ]), shadow="sm", p="md", radius="md"),
                span=4
            ),
            dmc.GridCol(
                dmc.Paper(dmc.Stack([
                    dmc.Text("Unidades Vendidas", size="sm", fw=500),
                    dmc.Text(f"{total_unidades:,}", size="xl", fw=700)
                ]), shadow="sm", p="md", radius="md"),
                span=4
            ),
            dmc.GridCol(
                dmc.Paper(dmc.Stack([
                    dmc.Text("Ticket Promedio (Q)", size="sm", fw=500),
                    dmc.Text(f"Q{ticket_promedio:,.2f}", size="xl", fw=700)
                ]), shadow="sm", p="md", radius="md"),
                span=4
            ),
        ], gutter="xl", mb=30),

        # Gráficas
        dmc.Grid([
            dmc.GridCol(dcc.Graph(figure=fig_campania), span=6),
            dmc.GridCol(dcc.Graph(figure=fig_pais), span=6),
        ], gutter="xl", mb=30),

        # Tabla detalle (agrupado por país y campaña)
        dmc.Table(
            [
                html.Thead(html.Tr([
                    html.Th("Campaña"),
                    html.Th("País"),
                    html.Th("Unidades"),
                    html.Th("Valor Q"),
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td(r.get("campania_legible", "N/A")),
                        html.Td(r["pais"]),
                        html.Td(r["unidades"]),
                        html.Td(f"Q{r['valor_q']:.2f}")
                    ]) for r in registros[:50]  # 👈 muestra hasta 20 filas agrupadas
                ])
            ],
            striped=True,
            highlightOnHover=True,
            withTableBorder=True,
            mb=30
        )
    ])

    return layout_base(contenido)

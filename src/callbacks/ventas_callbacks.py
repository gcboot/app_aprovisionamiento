from dash import Input, Output, State, html, no_update, dash_table
import dash_mantine_components as dmc
from src.models import ventas_raw, ventas
import base64, io, pandas as pd


def register_ventas_callbacks(app):

    # ---------- Renderizar tabla de ventas ----------
    def render_tabla_ventas(filtros=None):
        registros = ventas.get_ventas(filtros)
        if not registros:
            return dmc.Alert("No hay ventas procesadas.", color="yellow", variant="filled")

        rows = []
        for r in registros:
            rows.append(
                html.Tr([
                    html.Td(r.get("codigo_venta")),
                    html.Td(f"{r.get('codigo')} - {r.get('productos', {}).get('nombre', '')}"),
                    html.Td(f"C{r['campanias']['campania']} {r['campanias']['anio']}"),
                    html.Td(r.get("pais")),
                    html.Td(r.get("fecha")),
                    html.Td(r.get("unidades")),
                    html.Td(f"Q{r['precio_unitario']:.2f}" if r.get("precio_unitario") else ""),
                    html.Td(f"Q{r['valor_q']:.2f}" if r.get("valor_q") else ""),
                ])
            )

        return dmc.ScrollArea(
            offsetScrollbars=True,
            type="scroll",
            h=400,
            children=dmc.Table(
                striped=True,
                highlightOnHover=True,
                withBorder=True,
                withColumnBorders=True,
                children=[
                    html.Thead(html.Tr([
                        html.Th("Código Venta"),
                        html.Th("Producto"),
                        html.Th("Campaña"),
                        html.Th("País"),
                        html.Th("Fecha"),
                        html.Th("Unidades"),
                        html.Th("Precio Unitario"),
                        html.Th("Valor Q"),
                    ])),
                    html.Tbody(rows)
                ]
            )
        )

    # ---------- Renderizar tabla de eventos ----------
    def render_tabla_eventos(filtros=None):
        registros = ventas.get_eventos(filtros)
        if not registros:
            return dmc.Alert("No hay eventos de venta.", color="yellow", variant="filled")

        rows = []
        for r in registros:
            rows.append(
                html.Tr([
                    html.Td(r.get("id")),
                    html.Td(r.get("id_venta")),
                    html.Td(r.get("tipo_evento")),
                    html.Td(r.get("unidades")),
                    html.Td(f"Q{r['valor_q']:.2f}" if r.get("valor_q") else ""),
                    html.Td(r.get("fecha")),
                ])
            )

        return dmc.ScrollArea(
            offsetScrollbars=True,
            type="scroll",
            h=300,
            children=dmc.Table(
                striped=True,
                highlightOnHover=True,
                withBorder=True,
                withColumnBorders=True,
                children=[
                    html.Thead(html.Tr([
                        html.Th("ID Evento"),
                        html.Th("ID Venta"),
                        html.Th("Tipo Evento"),
                        html.Th("Unidades"),
                        html.Th("Valor Q"),
                        html.Th("Fecha"),
                    ])),
                    html.Tbody(rows)
                ]
            )
        )

    # ---------- Subir CSV a staging ----------
    @app.callback(
        Output("preview-staging", "children"),
        Input("upload-ventas", "contents"),
        State("upload-ventas", "filename"),
        prevent_initial_call=True
    )
    def cargar_staging(contents, filename):
        if not contents:
            return dmc.Alert("No se cargó archivo.", color="red")

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string).decode("utf-8")

        try:
            df_preview = ventas_raw.cargar_csv_ventas(decoded)
        except Exception as e:
            return dmc.Alert(f"Error cargando CSV: {str(e)}", color="red")

        # Mostrar tabla de preview
        return html.Div([
            dmc.Alert(f"Archivo {filename} cargado correctamente.", color="green", mb=10),
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df_preview.columns],
                data=df_preview.to_dict("records"),
                page_size=5,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "center"}
            )
        ])

    # ---------- Procesar staging ----------
    @app.callback(
        Output("resultado-etl", "children"),
        Input("btn-procesar-staging", "n_clicks"),
        prevent_initial_call=True
    )
    def procesar_etl(n):
        resumen = ventas.procesar_staging()
        return dmc.Alert(
            f"Procesadas {resumen['ventas_insertadas']} ventas y {resumen['eventos_insertados']} eventos.",
            color="blue"
        )

    # ---------- Filtros para ventas ----------
    @app.callback(
        Output("tabla-ventas", "children"),
        Input("btn-filtrar-ventas", "n_clicks"),
        State("filtro-campania", "value"),
        State("filtro-pais", "value"),
        State("filtro-producto", "value"),
        State("filtro-fechas", "value"),
        prevent_initial_call=True
    )
    def filtrar_ventas(n, campania, pais, producto, fechas):
        filtros = {}
        if campania:
            filtros["id_campania"] = campania
        if pais:
            filtros["pais"] = pais
        if producto:
            filtros["codigo"] = producto
        # Nota: supabase-py no soporta directamente gte/lte,
        # habría que manejar fechas con between en la función SQL
        return render_tabla_ventas(filtros)

    # ---------- Filtros para eventos ----------
    @app.callback(
        Output("tabla-eventos", "children"),
        Input("btn-filtrar-eventos", "n_clicks"),
        State("filtro-tipo-evento", "value"),
        State("filtro-campania-evento", "value"),
        State("filtro-producto-evento", "value"),
        prevent_initial_call=True
    )
    def filtrar_eventos(n, tipo_evento, campania, producto):
        filtros = {}
        if tipo_evento:
            filtros["tipo_evento"] = tipo_evento
        if campania:
            filtros["id_campania"] = campania
        if producto:
            filtros["codigo"] = producto
        return render_tabla_eventos(filtros)

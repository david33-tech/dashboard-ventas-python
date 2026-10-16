from pathlib import Path

import pandas as pd
import plotly.express as px


MESES = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
]
VENTAS = [12_000, 15_000, 11_000, 18_000, 22_000, 26_000, 24_000, 30_000]
GASTOS = [8_000, 9_000, 7_500, 10_000, 12_000, 14_000, 13_000, 16_000]

DIRECTORIO_SALIDA = Path(__file__).resolve().parent
ARCHIVO_CSV = DIRECTORIO_SALIDA / "reporte_ventas_dashboard.csv"
ARCHIVO_HTML = DIRECTORIO_SALIDA / "dashboard_ventas.html"


def crear_tabla_ventas() -> pd.DataFrame:
    """Construye la tabla de ventas y calcula la ganancia mensual."""
    tabla = pd.DataFrame(
        {
            "mes": MESES,
            "ventas": VENTAS,
            "gastos": GASTOS,
        }
    )
    tabla["ganancia"] = tabla["ventas"] - tabla["gastos"]
    return tabla


def imprimir_resumen(tabla: pd.DataFrame) -> None:
    """Imprime la tabla y los principales indicadores del periodo."""
    ventas_totales = tabla["ventas"].sum()
    gastos_totales = tabla["gastos"].sum()
    ganancia_total = tabla["ganancia"].sum()
    mejor_mes = tabla.loc[tabla["ganancia"].idxmax()]
    peor_mes = tabla.loc[tabla["ganancia"].idxmin()]

    print("\nREPORTE DE VENTAS")
    print(tabla.to_string(index=False))

    print("\nRESUMEN")
    print(f"Ventas totales:  ${ventas_totales:,.2f} MXN")
    print(f"Gastos totales:  ${gastos_totales:,.2f} MXN")
    print(f"Ganancia total:  ${ganancia_total:,.2f} MXN")
    print(
        f"Mejor mes:       {mejor_mes['mes']} "
        f"(${mejor_mes['ganancia']:,.2f} MXN)"
    )
    print(
        f"Mes con menor ganancia: {peor_mes['mes']} "
        f"(${peor_mes['ganancia']:,.2f} MXN)"
    )


def guardar_reporte_csv(tabla: pd.DataFrame) -> None:
    """Guarda la tabla de resultados en formato CSV."""
    tabla.to_csv(ARCHIVO_CSV, index=False, encoding="utf-8")
    print(f"\nReporte CSV guardado en: {ARCHIVO_CSV}")


def crear_dashboard(tabla: pd.DataFrame) -> None:
    """Genera y guarda el gráfico interactivo de ventas, gastos y ganancias."""
    figura = px.bar(
        tabla,
        x="mes",
        y=["ventas", "gastos", "ganancia"],
        barmode="group",
        title="Ventas, gastos y ganancia por mes",
        labels={
            "value": "Importe (MXN)",
            "mes": "Mes",
            "variable": "Concepto",
        },
        color_discrete_map={
            "ventas": "#2563EB",
            "gastos": "#F97316",
            "ganancia": "#16A34A",
        },
        template="plotly_white",
    )
    figura.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        legend_title_text="Concepto",
    )
    figura.write_html(ARCHIVO_HTML)
    print(f"Dashboard HTML guardado en: {ARCHIVO_HTML}")
    figura.show()


def main() -> None:
    tabla = crear_tabla_ventas()
    imprimir_resumen(tabla)
    guardar_reporte_csv(tabla)
    crear_dashboard(tabla)


if __name__ == "__main__":
    main()

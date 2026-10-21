"""Gráficos de la aplicación (equivalente a las gráficos de JFreeChart en Java).

En el proyecto Java los reportes se dibujaban con **JFreeChart**
(``ChartFactory.createPieChart3D`` y ``ChartFactory.createBarChart3D``) y se
incrustaban en un ``ChartPanel``. Aquí se usa **matplotlib**, que se integra
en Tkinter mediante ``FigureCanvasTkAgg`` (el mismo patrón que
``matplotlib.backends.backend_tkagg``).

Dependencia: ``pip install matplotlib``
"""

import logging

import matplotlib

# Necesario en Windows para que las fuentes se rendericen bien.
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

logger = logging.getLogger(__name__)

# Colores por defecto para cada estado de salud (se usan en los tres gráficos).
STATUS_COLORS = {
    "Sick": "#e74c3c",
    "Healthy": "#27ae60",
    "In Surgery": "#f39c12",
}
DEFAULT_COLOR = "#3498db"


def _colors_for(labels):
    """Devuelve un color por cada etiqueta (manteniendo el orden)."""
    return [STATUS_COLORS.get(label, DEFAULT_COLOR) for label in labels]


def build_pie_figure(report, title: str = "Pets Classification By health status") -> Figure:
    """Gráfico circular 3D (equivalente a ``createPieChart3D``)."""
    labels = [record.health_status for record in report]
    values = [record.amount_of_pets_by_health_status for record in report]

    figure = Figure(figsize=(6, 4.2), dpi=100)
    axes = figure.add_subplot(111)

    if values and any(values):
        axes.pie(
            values,
            labels=labels,
            colors=_colors_for(labels),
            autopct="%1.1f%%",
            shadow=True,
            startangle=90,
            wedgeprops={"edgecolor": "white"},
        )
        axes.axis("equal")
    else:
        axes.text(0.5, 0.5, "No hay datos para mostrar",
                  ha="center", va="center", fontsize=12, color="#7f8c8d")

    axes.set_title(title)
    figure.tight_layout()
    return figure


def build_bar_figure(report, title: str, xlabel: str, ylabel: str,
                     orientation: str = "vertical") -> Figure:
    """Gráfico de barras 3D (equivalente a ``createBarChart3D``).

    ``orientation`` puede ser ``"vertical"`` (perros) u ``"horizontal"`` (gatos).
    """
    labels = [record.health_status for record in report]
    values = [record.amount_of_pets_by_health_status for record in report]

    figure = Figure(figsize=(6, 4.2), dpi=100)
    axes = figure.add_subplot(111)

    if labels:
        colors = _colors_for(labels)
        if orientation == "horizontal":
            bars = axes.barh(labels, values, color=colors, edgecolor="white")
            axes.set_xlabel(xlabel)
            axes.set_ylabel(ylabel)
            axes.invert_yaxis()
        else:
            bars = axes.bar(labels, values, color=colors, edgecolor="white")
            axes.set_xlabel(xlabel)
            axes.set_ylabel(ylabel)
            axes.set_ylim(0, max(values) + 1)

        # Etiqueta con el valor encima de cada barra.
        for bar, value in zip(bars, values):
            if orientation == "horizontal":
                axes.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                          str(value), va="center", fontsize=9)
            else:
                axes.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                          str(value), ha="center", fontsize=9)
    else:
        axes.text(0.5, 0.5, "No hay datos para mostrar",
                  ha="center", va="center", fontsize=12, color="#7f8c8d")

    axes.set_title(title)
    figure.tight_layout()
    return figure


class ChartFrame:
    """Contenedor de un gráfico dentro de un frame de Tkinter.

    Reemplaza al ``ChartPanel`` de JFreeChart. Permite redibujar el gráfico
    (``set_report``) destruyendo el canvas anterior, tal como se hacía en Java
    con ``panel.removeAll()`` + ``repaint()``.
    """

    def __init__(self, parent, figure: Figure | None = None):
        from tkinter import ttk

        self.parent = parent
        self.figure = figure
        self.canvas = None
        self.toolbar = None

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        if figure is not None:
            self._draw(figure)

    def _draw(self, figure: Figure) -> None:
        """Crea (o reemplaza) el canvas con la figura indicada."""
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if self.toolbar is not None:
            self.toolbar.destroy()
            self.toolbar = None

        self.canvas = FigureCanvasTkAgg(figure, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # La firma de ``NavigationToolbar2Tk`` cambió entre versiones de
        # matplotlib (el parámetro ``pack_toolbar`` se añadió en 3.8), por eso
        # se usa un ``try/except`` para funcionar con cualquiera de las dos.
        try:
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame,
                                                pack_toolbar=False)
        except TypeError:
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
            self.toolbar.pack_forget()
        self.toolbar.update()
        self.toolbar.pack(fill="x", side="bottom")

    def set_figure(self, figure: Figure) -> None:
        """Reemplaza el gráfico actual por otro."""
        self.figure = figure
        self._draw(figure)

    def clear(self) -> None:
        """Elimina el gráfico actual."""
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if self.toolbar is not None:
            self.toolbar.destroy()
            self.toolbar = None


__all__ = [
    "ChartFrame",
    "build_bar_figure",
    "build_pie_figure",
]

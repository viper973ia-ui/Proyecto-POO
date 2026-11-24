import numpy as np
import matplotlib.pyplot as plt

from matplotlib.lines import Line2D
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


# ============================================================
# EJEMPLO 1. AGRUPACIÓN DE TRAMOS POR ESTADO Y TRÁFICO
# ============================================================
# Todos los datos son simulados.
#
# Cada fila representa un tramo.
# Columnas:
#   IRI: irregularidad longitudinal, en m/km.
#   Fisuración: porcentaje de superficie fisurada.
#   Roderas: profundidad en mm.
#   Edad: años desde la actuación de referencia.
#   IMD: intensidad media diaria, vehículos/día.
#   Pesados: porcentaje de vehículos pesados.
#
# No se establecen umbrales normativos ni tratamientos automáticos.

tramos = np.array([
    "T01", "T02", "T03",
    "T04", "T05", "T06",
    "T07", "T08", "T09",
    "T10", "T11", "T12",
])

variables = [
    "IRI\n(m/km)",
    "Fisuración\n(%)",
    "Roderas\n(mm)",
    "Edad\n(años)",
    "IMD\n(veh/día)",
    "Pesados\n(%)",
]

datos = np.array([
    [1.4,  2,  3,  3,  42000, 12],
    [1.6,  3,  4,  4,  39000, 13],
    [1.5,  2,  3,  3,  51000, 11],

    [2.0,  6,  6,  7,  98000,  6],
    [2.2,  7,  7,  8, 105000,  6],
    [1.9,  5,  5,  6,  91000,  5],

    [2.6,  9, 16,  9,  26000, 22],
    [2.9, 11, 19, 10,  24000, 24],
    [2.4,  8, 14,  8,  28000, 21],

    [3.9, 18,  9, 14,  11000,  9],
    [4.4, 24, 11, 16,   9500, 10],
    [3.6, 15,  8, 13,  12500,  8],
], dtype=float)


# Estandarización:
# evita que la IMD domine el análisis solo por su escala numérica.
media = datos.mean(axis=0)
desviacion = datos.std(axis=0)

# Protección frente a columnas constantes.
desviacion[desviacion == 0] = 1.0

datos_normalizados = (datos - media) / desviacion

# Agrupamiento jerárquico con Ward.
Z = linkage(datos_normalizados, method="ward")

# Se eligen cuatro grupos para esta demostración.
# En una aplicación real hay que justificar y validar esta elección.
numero_grupos = 4
grupos = fcluster(Z, t=numero_grupos, criterion="maxclust")

# Altura de corte situada entre las fusiones correspondientes.
altura_inferior = Z[-numero_grupos, 2]
altura_superior = Z[-(numero_grupos - 1), 2]
altura_corte = (altura_inferior + altura_superior) / 2

fig1, (ax_arbol, ax_perfiles) = plt.subplots(
    1, 2, figsize=(15, 6)
)

resultado_arbol = dendrogram(
    Z,
    labels=tramos.tolist(),
    color_threshold=altura_corte,
    above_threshold_color="gray",
    ax=ax_arbol,
)

ax_arbol.axhline(
    altura_corte,
    color="black",
    linestyle="--",
    label="Corte ilustrativo para 4 grupos",
)
ax_arbol.set_title("Agrupamiento de tramos")
ax_arbol.set_xlabel("Tramo")
ax_arbol.set_ylabel("Altura de fusión de Ward")
ax_arbol.legend(fontsize=8)

# Ordenar el mapa de calor igual que las hojas del árbol.
orden = resultado_arbol["leaves"]
datos_ordenados = datos_normalizados[orden]

limite = max(1.0, float(np.abs(datos_normalizados).max()))

imagen = ax_perfiles.imshow(
    datos_ordenados,
    cmap="RdBu_r",
    vmin=-limite,
    vmax=limite,
    aspect="auto",
)

ax_perfiles.set_xticks(np.arange(len(variables)))
ax_perfiles.set_xticklabels(variables, fontsize=8)
ax_perfiles.set_yticks(np.arange(len(tramos)))
ax_perfiles.set_yticklabels([
    f"{tramos[i]} · G{grupos[i]}" for i in orden
])
ax_perfiles.set_title("Perfil de cada tramo: valores estandarizados")

barra = fig1.colorbar(imagen, ax=ax_perfiles, shrink=0.8)
barra.set_label("Desviaciones típicas respecto a la media")

fig1.suptitle(
    "Ejemplo 1 · Familias de tramos · DATOS SIMULADOS",
    fontsize=13,
)
fig1.tight_layout(rect=[0, 0, 1, 0.94])

print("\nEJEMPLO 1: GRUPOS DE TRAMOS")
print("=" * 65)

for grupo in sorted(np.unique(grupos)):
    seleccion = grupos == grupo
    promedios = datos[seleccion].mean(axis=0)

    print(f"\nGrupo {grupo}: {', '.join(tramos[seleccion])}")
    print(
        f"  IRI: {promedios[0]:.2f} m/km | "
        f"Fisuración: {promedios[1]:.1f}% | "
        f"Roderas: {promedios[2]:.1f} mm"
    )
    print(
        f"  Edad: {promedios[3]:.1f} años | "
        f"IMD: {promedios[4]:.0f} veh/día | "
        f"Pesados: {promedios[5]:.1f}%"
    )

print("\nLos números de grupo son etiquetas, no niveles de prioridad.")


# ============================================================
# EJEMPLO 2. ASIGNACIÓN A BASES DE CONSERVACIÓN
# ============================================================
# Red simplificada de 12 nodos.
# Las coordenadas están expresadas en km.
#
# Entre la fila inferior y la intermedia solo hay conexiones
# en los extremos: representa una barrera con dos pasos.
#
# Las conexiones son bidireccionales.
# Se supone una velocidad uniforme de 60 km/h.
# No se incluyen sentidos únicos, congestión ni restricciones.

coordenadas = np.array([
    [ 0,  0], [ 4,  0], [ 8,  0], [12,  0],
    [ 0,  6], [ 4,  6], [ 8,  6], [12,  6],
    [ 0, 12], [ 4, 12], [ 8, 12], [12, 12],
], dtype=float)

# Cada pareja identifica una carretera entre dos nodos.
aristas = [
    # Conexiones horizontales.
    (0, 1), (1, 2), (2, 3),
    (4, 5), (5, 6), (6, 7),
    (8, 9), (9, 10), (10, 11),

    # Pasos entre fila inferior e intermedia.
    (0, 4), (3, 7),

    # Conexiones entre fila intermedia y superior.
    (4, 8), (5, 9), (6, 10), (7, 11),
]

# Las bases se sitúan en tres nodos de la red.
nodos_bases = np.array([0, 3, 9])
nombres_bases = ["Base A", "Base B", "Base C"]
colores = ["tab:blue", "tab:orange", "tab:green"]

n_nodos = len(coordenadas)
matriz_distancias = np.zeros((n_nodos, n_nodos))

for origen, destino in aristas:
    longitud = np.linalg.norm(
        coordenadas[origen] - coordenadas[destino]
    )
    matriz_distancias[origen, destino] = longitud
    matriz_distancias[destino, origen] = longitud

grafo = csr_matrix(matriz_distancias)

# Distancia mínima POR CARRETERA desde cada base.
distancias_red = dijkstra(
    grafo,
    directed=False,
    indices=nodos_bases,
)

if not np.isfinite(distancias_red).all():
    raise ValueError(
        "La red tiene nodos desconectados. Revisa las conexiones."
    )

# Distancia EN LÍNEA RECTA desde cada base.
distancias_rectas = np.linalg.norm(
    coordenadas[nodos_bases, None, :]
    - coordenadas[None, :, :],
    axis=2,
)

asignacion_recta = np.argmin(distancias_rectas, axis=0)
asignacion_red = np.argmin(distancias_red, axis=0)

# Si hay empate, argmin elige la primera base de la lista.
# En explotación habría que definir una regla de desempate.
velocidad_kmh = 60.0
tiempos_minimos = (
    distancias_red.min(axis=0) / velocidad_kmh * 60
)

cambios = asignacion_recta != asignacion_red

fig2, ejes = plt.subplots(1, 2, figsize=(14, 6))

# Voronoi plano: sus fronteras se dibujan solo en el panel izquierdo.
voronoi = Voronoi(coordenadas[nodos_bases])

voronoi_plot_2d(
    voronoi,
    ax=ejes[0],
    show_points=False,
    show_vertices=False,
    line_colors="gray",
    line_width=1.5,
    line_alpha=0.8,
)

for ax, asignacion, titulo in zip(
    ejes,
    [asignacion_recta, asignacion_red],
    [
        "Línea recta: Voronoi plano",
        "Por carretera: asignación sobre la red",
    ],
):
    # Dibujar carreteras.
    for origen, destino in aristas:
        ax.plot(
            coordenadas[[origen, destino], 0],
            coordenadas[[origen, destino], 1],
            color="lightgray",
            linewidth=3,
            zorder=1,
        )

    # Colorear cada punto según su base asignada.
    for indice_base, color in enumerate(colores):
        seleccion = asignacion == indice_base
        ax.scatter(
            coordenadas[seleccion, 0],
            coordenadas[seleccion, 1],
            color=color,
            s=80,
            zorder=3,
        )

    # Identificadores de los puntos.
    for nodo, (x, y) in enumerate(coordenadas):
        ax.annotate(
            f"P{nodo:02d}",
            (x, y),
            xytext=(5, 7),
            textcoords="offset points",
            fontsize=8,
        )

    # Marcar bases.
    for indice_base, nodo in enumerate(nodos_bases):
        ax.scatter(
            *coordenadas[nodo],
            marker="*",
            s=300,
            color=colores[indice_base],
            edgecolor="black",
            zorder=5,
        )

    ax.set_title(titulo)
    ax.set_xlabel("Coordenada X (km)")
    ax.set_ylabel("Coordenada Y (km)")
    ax.set_aspect("equal")
    ax.set_xlim(-2, 15)
    ax.set_ylim(-2, 15)
    ax.grid(alpha=0.2)

# Rodear los puntos cuya asignación cambia.
ejes[1].scatter(
    coordenadas[cambios, 0],
    coordenadas[cambios, 1],
    facecolors="none",
    edgecolors="black",
    s=240,
    linewidths=1.5,
    zorder=4,
)

leyenda = [
    Line2D(
        [0], [0],
        marker="o",
        color="none",
        markerfacecolor=color,
        markeredgecolor=color,
        label=nombre,
        markersize=8,
    )
    for nombre, color in zip(nombres_bases, colores)
]

leyenda.extend([
    Line2D(
        [0], [0],
        marker="*",
        color="none",
        markerfacecolor="gray",
        markeredgecolor="black",
        label="Ubicación de una base",
        markersize=13,
    ),
    Line2D(
        [0], [0],
        marker="o",
        color="none",
        markerfacecolor="none",
        markeredgecolor="black",
        label="Cambia la base asignada",
        markersize=11,
    ),
])

fig2.legend(
    handles=leyenda,
    loc="lower center",
    ncol=3,
    fontsize=8,
)

fig2.suptitle(
    "Ejemplo 2 · Cobertura de bases · RED SIMULADA",
    fontsize=13,
)
fig2.tight_layout(rect=[0, 0.12, 1, 0.94])

print("\n\nEJEMPLO 2: ASIGNACIÓN DE PUNTOS A BASES")
print("=" * 65)
print(
    f"{'Punto':<8}"
    f"{'Línea recta':<15}"
    f"{'Por carretera':<16}"
    f"{'Minutos':>9}"
)

for nodo in range(n_nodos):
    base_recta = nombres_bases[asignacion_recta[nodo]]
    base_red = nombres_bases[asignacion_red[nodo]]

    print(
        f"P{nodo:02d}     "
        f"{base_recta:<15}"
        f"{base_red:<16}"
        f"{tiempos_minimos[nodo]:>9.1f}"
    )

print(
    f"\nPuntos con distinta asignación: "
    f"{np.count_nonzero(cambios)} de {n_nodos}"
)
print("En los empates se elige la primera base de la lista.")

plt.show()
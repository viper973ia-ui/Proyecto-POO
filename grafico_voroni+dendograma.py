import numpy as np, matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.cluster.hierarchy import linkage, dendrogram

rng = np.random.default_rng(7)
pts = rng.random((30, 2))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.5))
voronoi_plot_2d(Voronoi(pts), ax=a1, show_vertices=False)
a1.set_title("Voronoi")
dendrogram(linkage(pts, "ward"), ax=a2)
a2.set_title("Dendrograma")
plt.tight_layout(); plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng(5)
n = 150
cil = rng.choice([4, 6, 8], n, p=[0.5, 0.3, 0.2])
coches = pd.DataFrame({"potencia": cil * 18 + rng.normal(0, 12, n),
"peso": cil * 230 + rng.normal(0, 150, n),
"consumo": 2 + cil * 0.9 + rng.normal(0, 0.6, n),
"aceleracion": 20 - cil * 0.8 + rng.normal(0, 1.2, n)})
colores = pd.Series(cil).map({4: "#3776AB", 6: "#E0A800", 8:"#E07B39"})
ejes = pd.plotting.scatter_matrix(coches, figsize=(7, 7),diagonal="kde",c=colores, alpha=0.6, s=18)
plt.suptitle("Relaciones entre variables (azul 4, amarillo 6,naranja 8 cilindros)", y=0.92)
plt.show()
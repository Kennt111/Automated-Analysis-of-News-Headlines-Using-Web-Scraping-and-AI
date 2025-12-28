
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

with open("titulares_clasificados_multi_medio.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

for medio, categorias in data.items():
    for categoria, titulos in categorias.items():
        rows.append({
            "Medio": medio,
            "Categoria": categoria,
            "Cantidad": len(titulos)
        })

df_conteo = pd.DataFrame(rows)

# ❌ filtros
df_conteo = df_conteo[df_conteo["Categoria"] != "Otros"]
df_conteo = df_conteo[df_conteo["Medio"] != "EMOL"]

print(df_conteo)


heatmap_data = df_conteo.pivot(
    index="Medio",
    columns="Categoria",
    values="Cantidad"
).fillna(0)


heatmap_data_prop = heatmap_data.div(
    heatmap_data.sum(axis=1),
    axis=0
)


plt.figure(figsize=(10, 6))

sns.heatmap(
    heatmap_data_prop,
    annot=True,
    fmt=".2f",
    cmap="Reds",
    linewidths=0.5,
    linecolor="white",
    mask=heatmap_data_prop < 0.05,  # oculta valores irrelevantes
    cbar_kws={"label": "Proporción"}
)


plt.title("Distribución proporcional de titulares por categoría (normalizado por medio)")
plt.ylabel("Medio")
plt.xlabel("Categoría")

plt.tight_layout()
plt.show()
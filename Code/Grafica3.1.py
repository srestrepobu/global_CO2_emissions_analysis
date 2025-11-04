import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# === Cargar dataset ===
EXCEL_PATH = "../Datos/EDGAR_2025_GHG_booklet_2025_fossilCO2only.xlsx"
SHEET = "fossil_CO2_totals_by_country"

df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET)

# === Limpiar columnas ===
df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

# === Transformar formato (wide → long) ===
df_long = df.melt(id_vars=["substance", "edgar_country_code", "country"],
                  value_vars=[col for col in df.columns if col.isdigit()],
                  var_name="year", value_name="fossil_co2_total")

df_long["year"] = pd.to_numeric(df_long["year"])
df_long = df_long[df_long["substance"] == "CO2"].dropna(subset=["fossil_co2_total"])

# === Seleccionar países relevantes ===
selected_countries = ["United States", "China", "India", "Russia", "Japan", "Colombia"]

df_long = df_long[df_long["country"].isin(selected_countries)]
df_long = df_long.sort_values(by=["year", "country"])

# === Filtrar valores positivos ===
df_long = df_long[df_long["fossil_co2_total"] > 0]

# === Crear figura ===
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(df_long["year"].min(), df_long["year"].max() + 10)
ax.set_ylim(-0.5, 14000)  # Ajuste del límite Y
ax.set_xlabel("Year")
ax.set_ylabel("Fossil CO₂ emissions (MtCO₂)")
ax.set_title("CO₂ Emissions — Top Emitters in America + Global Trend")

# === Asignar colores ===
cmap = plt.colormaps.get_cmap("tab10")
countries = df_long["country"].unique()
colors = [cmap(i / len(countries)) for i in range(len(countries))]

# === Inicializar líneas y etiquetas ===
lines, labels = {}, {}

for i, country in enumerate(countries):
    style = {"color": colors[i], "lw": 2} if country != "Colombia" else {"color": colors[i], "lw": 3.2}
    line, = ax.plot([], [], label=country, **style)
    lines[country] = line
    labels[country] = ax.text(df_long["year"].max() + 2, 0, "", fontsize=9, color=style["color"], va="center")

# === Leyenda fija ===
ax.legend(loc="center left", bbox_to_anchor=(-0.23, 0.5), fontsize="small", title="Countries")
plt.subplots_adjust(left=0.18, right=0.93)

# === Años y datos únicos ===
years = sorted(df_long["year"].unique())


# === Función para ordenar etiquetas ===
def ordenar_etiquetas(posiciones):
    """Evita que las etiquetas se superpongan verticalmente al final."""
    posiciones_ordenadas = sorted(posiciones, key=lambda x: x[1])
    separacion_min = 0.03 * ax.get_ylim()[1]
    for i in range(1, len(posiciones_ordenadas)):
        if posiciones_ordenadas[i][1] - posiciones_ordenadas[i - 1][1] < separacion_min:
            posiciones_ordenadas[i] = (posiciones_ordenadas[i][0], posiciones_ordenadas[i - 1][1] + separacion_min,
                                       posiciones_ordenadas[i][2])

    return {p[2]: (p[0], p[1]) for p in posiciones_ordenadas}


# === Función de actualización ===
def update(frame):
    year = years[frame]
    ax.set_title(f"Top Emitters + Colombia — {year}")

    posiciones = []
    for country in countries:
        data = df_long[df_long["country"] == country]
        past = data[data["year"] <= year]
        lines[country].set_data(past["year"], past["fossil_co2_total"])

        if not past.empty:
            x = past["year"].iloc[-1]
            y = past["fossil_co2_total"].iloc[-1]
            posiciones.append((x + 2, y, country))

    # Si estamos en los últimos cuadros, ordenar etiquetas verticalmente
    if frame == len(years) - 1:
        ordenadas = ordenar_etiquetas(posiciones)
        for country, (x, y) in ordenadas.items():
            labels[country].set_position((x, y))
            labels[country].set_text(country)
    else:
        for (x, y, country) in posiciones:
            labels[country].set_position((x, y))
            labels[country].set_text(country)

    return list(lines.values()) + list(labels.values())


# === Crear animación ===
ani = animation.FuncAnimation(fig, update, frames=len(years), interval=120, repeat=True)

# === Guardar GIF ===
ani.save("../Graphs/CO2_TopEmitters_Colombia.gif", writer="pillow", fps=7)
plt.show()
# === Guardar imagen final limpia ===
update(len(years) - 1)
plt.savefig("../Graphs/CO2_TopEmitters_Colombia_Final.jpg", dpi=400, bbox_inches="tight")

plt.show()

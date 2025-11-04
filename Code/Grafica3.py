
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.cm as cm

# ===============================
# Load data from Excel file
# ===============================
# Reads the Excel sheet named “fossil_CO2_totals_by_country”
# which contains CO₂ emissions per country per year.
file_path = "../Datos/EDGAR_2025_GHG_booklet_2025_fossilCO2only.xlsx"
sheet_name = "fossil_CO2_totals_by_country"

df = pd.read_excel(file_path, sheet_name=sheet_name)

# ===============================
# Filter only South American countries
# ===============================
# We create a list of South American countries and keep
# only their emission values for 2024.
south_america = [
    'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador',
    'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela'
]
df_south = df[df["Country"].isin(south_america)][["Country", 2024]].rename(columns={2024: "CO2"})

# ===============================
# Load the world map using GeoPandas
# ===============================
# The map is loaded from the Natural Earth dataset (in GeoJSON format).
# Then we extract only the South American continent and merge
# the geographic information with the CO₂ emission data.
world = gpd.read_file(
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
)
geo = world[world["CONTINENT"] == "South America"].merge(df_south, how="left", left_on="NAME_EN", right_on="Country")

# ===============================
# Assign unique colors using tab20
# ===============================
# The colormap "tab20b" provides up to 20 easily distinguishable colors.
# Each country will receive a unique color from this palette.
cmap = cm.get_cmap('tab20b', len(geo))

# Drop countries with missing CO₂ values and reset index
geo = geo.dropna(subset=["CO2"]).reset_index(drop=True)

# ===============================
# Sort geo dataframe by CO2 emissions
# ===============================
geo_sorted = geo.sort_values(by="CO2", ascending=True)  # Sort countries by CO2 emissions

# Assign a color from the colormap to each country
geo_sorted["color"] = [cmap(i) for i in range(len(geo_sorted))]  # Assign colors to the sorted dataframe

# ===============================
# Create the main figure
# ===============================
# The map is drawn with soft background color and white borders.
fig, ax = plt.subplots(figsize=(14, 9))
fig.patch.set_facecolor("#fafafa")

geo_sorted.plot(color=geo_sorted["color"], linewidth=1.2, edgecolor="white", ax=ax)

# ===============================
# Determine label color dynamically
# ===============================
# This function calculates the perceived brightness (luminance)
# of each country's color and automatically chooses black or white text
# for optimal readability.
def get_text_color(country):
    country_color = geo_sorted.loc[geo_sorted['Country'] == country, 'color'].values[0]
    r, g, b, _ = country_color
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "black" if luminance > 0.6 else "white"

# ===============================
# Add country labels to the map
# ===============================
# Labels are placed at the centroid of each country shape.
# Some are slightly offset to prevent overlap.
label_offsets = {
    "GUY": (0.8, 0.8),
    "SUR": (-0.8, -0.8)
}

for _, row in geo_sorted.iterrows():
    if pd.isna(row["CO2"]):
        continue
    centroid = row["geometry"].representative_point()
    iso = row["ISO_A3"]
    dx, dy = label_offsets.get(iso, (0, 0))
    label = f"{iso}\n{row['CO2']:.0f} Mt"  # ISO code and emission value (in megatonnes)
    color_text = get_text_color(row["Country"])
    ax.text(
        centroid.x + dx, centroid.y + dy, label,
        ha="center", va="center", fontsize=10.5,
        color=color_text,
        path_effects=[path_effects.withStroke(linewidth=1.2, foreground="black", alpha=0.3)]
    )

# --- Map title and formatting ---
ax.set_title(
    "CO₂ Emissions by Country in South America (2024)",
    fontsize=22, color="#222", pad=20
)
ax.axis("off")

# Automatically adjust the map limits to include all countries nicely
bounds = geo_sorted.total_bounds
ax.set_xlim(bounds[0] - 5, bounds[2] + 5)
ax.set_ylim(bounds[1] - 5, bounds[3] + 5)

# ===============================
# Add the inset barplot (bottom-right corner)
# ===============================
# The barplot compares emission magnitudes between countries.
# It’s embedded inside the same figure using inset_axes().
ax_inset = inset_axes(ax, width="38%", height="25%", loc="lower right", borderpad=2)

# Sort countries by CO₂ emissions (ascending)
bar_colors = geo_sorted["color"]

# Horizontal barplot with the same color as the map
ax_inset.barh(geo_sorted["Country"], geo_sorted["CO2"], color=bar_colors, edgecolor="none", height=0.55)

# --- Barplot style adjustments ---
ax_inset.set_facecolor("#fafafa")
ax_inset.tick_params(axis="x", labelsize=8)
ax_inset.tick_params(axis="y", labelsize=8)
ax_inset.set_xlabel("Emissions (Mt)", fontsize=9, labelpad=4)
ax_inset.set_ylabel("", fontsize=9)

# Remove unnecessary borders
for spine in ["top", "right", "left", "bottom"]:
    ax_inset.spines[spine].set_visible(False)

ax_inset.grid(False)

# ===============================
# Save and display the final figure
# ===============================
# The final image is exported at high resolution (300 dpi)
# and displayed on screen.
plt.tight_layout()
plt.savefig("../Graphs/mapa_CO2_Sudamerica.png", dpi=300, bbox_inches="tight")
plt.show()

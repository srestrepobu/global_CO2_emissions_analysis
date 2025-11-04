import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
archivo = '../Datos/EDGAR_2025_GHG_booklet_2025_fossilCO2only.xlsx'

# Read the "fossil_CO2_by_sector_country_su" sheet
df_sectores = pd.read_excel(archivo, sheet_name='fossil_CO2_by_sector_country_su')

# Extract rows 1462 to 1469 (indices 1461 to 1468 in pandas)
df_sectores_filtrado = df_sectores.iloc[1461:1469]

# Last 10 years to analyze
ultimos_10_años = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Define the order of sectors (bottom to top in the stacked bar)
sector_order = [
    'Power Industry',
    'Transport',
    'Industrial Combustion',
    'Buildings',
    'Processes',
    'Fuel Exploitation',
    'Waste',
    'Agriculture'
]

# Assign colors for each sector
colors = {
    'Power Industry': '#e74c3c',  # Red
    'Transport': '#3498db',  # Blue
    'Industrial Combustion': '#2ecc71',  # Green
    'Buildings': '#f39c12',  # Orange
    'Processes': '#9b59b6',  # Purple
    'Fuel Exploitation': '#1abc9c',  # Teal
    'Waste': '#95a5a6',  # Gray
    'Agriculture': '#e67e22',  # Dark orange
}

# Prepare data matrix for stacked bar plot
data_matrix = []

for sector in sector_order:
    sector_values = []
    for year in ultimos_10_años:
        # Find the row for this sector
        sector_row = df_sectores_filtrado[df_sectores_filtrado['Sector'] == sector]
        if not sector_row.empty and year in sector_row.columns:
            value = sector_row[year].values[0]
            if pd.notna(value) and value > 0:
                sector_values.append(value)
            else:
                sector_values.append(0)
        else:
            sector_values.append(0)
    data_matrix.append(sector_values)

# Convert to DataFrame for easier manipulation
df_plot = pd.DataFrame(data_matrix, index=sector_order, columns=ultimos_10_años).T

# Calculate totals per year
totals = df_plot.sum(axis=1)

# Create figure with extra space for legend
fig, ax = plt.subplots(figsize=(16, 8))
fig.patch.set_facecolor('white')

# Create stacked bar plot
bottom = np.zeros(len(ultimos_10_años))
bar_width = 0.6

for sector in sector_order:
    values = df_plot[sector].values
    bars = ax.bar(
        ultimos_10_años,
        values,
        bar_width,
        bottom=bottom,
        label=sector,
        color=colors[sector],
        edgecolor='white',
        linewidth=1.5
    )

    # Add text labels for larger segments (>5% of total)
    for i, (year, value) in enumerate(zip(ultimos_10_años, values)):
        if value > 0:
            percentage = (value / totals.iloc[i]) * 100
            if percentage > 5:  # Only label significant segments
                text_y = bottom[i] + value / 2
                ax.text(
                    year, text_y,
                    f'{int(value):,}',
                    ha='center', va='center',
                    fontsize=9, fontweight='bold',
                    color='white'
                )

    bottom += values

# Add total values on top of each bar
for i, (year, total) in enumerate(zip(ultimos_10_años, totals)):
    ax.text(
        year, total + 500,
        f'{int(total):,}',
        ha='center', va='bottom',
        fontsize=12, fontweight='bold',
        color='#2C3E50'
    )

# Customize axes
ax.set_xlabel('Year', fontsize=14, fontweight='bold', color='#2C3E50', labelpad=10)
ax.set_ylabel('Million tonnes CO₂', fontsize=14, fontweight='bold', color='#2C3E50', labelpad=10)
ax.set_title('Global CO₂ Emissions by Sector\nEvolution from 2015 to 2024',
             fontsize=20, fontweight='bold', color='#2C3E50', pad=20)

# Format y-axis
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
ax.tick_params(axis='both', labelsize=11, colors='#555555')

# Set x-axis ticks
ax.set_xticks(ultimos_10_años)
ax.set_xticklabels(ultimos_10_años, fontsize=12, fontweight='600')

# Grid
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7, color='#cccccc')
ax.set_axisbelow(True)

# Spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#999999')
ax.spines['bottom'].set_color('#999999')
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)

# Legend - positioned outside to the right
legend = ax.legend(
    loc='center left',
    bbox_to_anchor=(1.02, 0.5),
    ncol=1,
    frameon=True,
    fontsize=12,
    title='Sectors',
    title_fontsize=13,
    edgecolor='#cccccc',
    fancybox=True,
    shadow=True
)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_alpha(0.95)

# Adjust layout to accommodate legend
plt.subplots_adjust(right=0.82)

# Save figure
plt.savefig('../Graphs/co2_stacked_barplot.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')

plt.show()


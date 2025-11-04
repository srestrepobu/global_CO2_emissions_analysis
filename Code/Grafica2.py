import pandas as pd
import matplotlib.pyplot as plt
from pywaffle import Waffle
import numpy as np
import matplotlib.patches as mpatches

# Read the Excel file
# If you get an error like:
#   ImportError: Missing optional dependency 'openpyxl'
# it means you need to install the openpyxl library.
# Solution: open the terminal in your virtual environment and run:
#     pip install openpyxl
# or if you use conda:
#     conda install openpyxl
# After installing it, rerun the code and it should work fine.
archivo = '../Datos/EDGAR_2025_GHG_booklet_2025_fossilCO2only.xlsx'

# Read the "fossil_CO2_by_sector_country_su" sheet
df_sectores = pd.read_excel(archivo, sheet_name='fossil_CO2_by_sector_country_su')

# Extract rows 1462 to 1469 (indices 1461 to 1468 in pandas, since it starts from 0)
df_sectores_filtrado = df_sectores.iloc[1461:1469]

# Last 10 years to analyze
ultimos_10_años = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Define the order of sectors for consistency in plots
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
colors = [
    '#e74c3c',  # Power Industry - Red
    '#3498db',  # Transport - Blue
    '#2ecc71',  # Industrial Combustion - Green
    '#f39c12',  # Buildings - Orange
    '#9b59b6',  # Processes - Purple
    '#1abc9c',  # Fuel Exploitation - Teal
    '#95a5a6',  # Waste - Gray
    '#e67e22',  # Agriculture - Dark orange
]

# Prepare aggregated data by year
data_by_year = []

for year in ultimos_10_años:
    year_dict = {'year': year}
    total_year = 0

    # Iterate through filtered rows and extract CO2 values for each sector
    for _, row in df_sectores_filtrado.iterrows():
        sector_name = row['Sector']
        if sector_name in sector_order:
            try:
                value = float(row[year])
                if pd.notna(value) and value > 0:
                    year_dict[sector_name] = value
                    total_year += value
                else:
                    year_dict[sector_name] = 0
            except Exception as e:
                print(f"Error reading {sector_name} for year {year}: {e}")
                year_dict[sector_name] = 0

    # Add the total emissions for that year
    year_dict['total'] = total_year
    data_by_year.append(year_dict)

# Create aggregated DataFrame
df_agg = pd.DataFrame(data_by_year)


# Find the maximum total emissions to scale the waffle charts
max_year_value = df_agg['total'].max()

# Create the figure layout with proper spacing
ncols = len(ultimos_10_años)
fig = plt.figure(figsize=(24, 8))
fig.patch.set_facecolor('white')

# Use gridspec for better subplot layout control
import matplotlib.gridspec as gridspec

gs = gridspec.GridSpec(1, ncols, figure=fig,
                       left=0.08, right=0.95,
                       bottom=0.15, top=0.82,
                       wspace=0.08)

axs = [fig.add_subplot(gs[0, i]) for i in range(ncols)]

# Create waffle charts for each year
for idx, (year, ax) in enumerate(zip(ultimos_10_años, axs)):
    # Extract emission data for that year in the defined order
    year_data = df_agg[df_agg['year'] == year].iloc[0]

    values = []
    sector_names = []
    for sector in sector_order:
        if sector in year_data and year_data[sector] > 0:
            values.append(year_data[sector])
            sector_names.append(sector)

    # Sort values in descending order
    sorted_indices = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
    values = [values[i] for i in sorted_indices]

    # Compute total emissions for this year
    total_current = sum(values)

    # Add white filler to reach the same height as the maximum year
    values.append(max_year_value - total_current)

    # Sort colors to match values
    current_colors = [colors[sector_order.index(sector_names[i])] for i in sorted_indices]
    current_colors.append('white')

    # Create the waffle plot
    try:
        Waffle.make_waffle(
            ax=ax,
            rows=50,
            columns=10,
            values=values,
            vertical=True,
            colors=current_colors,
            block_arranging_style='snake',
            starting_location='SW',
            rounding_rule='nearest',
            interval_ratio_x=0.15,
            interval_ratio_y=0.15
        )
    except Exception as e:
        print(f"Error creating waffle for year {year}: {e}")
        continue

    # Add the year label below
    ax.text(x=0.5, y=-0.06, s=f"{int(year)}",
            fontsize=18, ha="center", fontweight='bold',
            transform=ax.transAxes, color='#2C3E50')

    # Add total emission value above
    ax.text(x=0.5, y=1.04, s=f"{int(total_current):,}",
            fontsize=14, ha="center", fontweight='bold',
            transform=ax.transAxes, color='#2C3E50')

    # Remove default spines for a cleaner look
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Hide x and y ticks
    ax.set_xticks([])
    ax.tick_params(axis='x', length=0)
    ax.set_yticks([])

# Add custom Y-axis to the first subplot
num_y_ticks = 6
y_tick_values = np.linspace(0, max_year_value, num_y_ticks)
y_tick_values = [int(val) for val in y_tick_values]

for y_tick in y_tick_values:
    # Add tick label
    axs[0].text(
        x=-0.25,
        y=y_tick / max_year_value,
        s=f"{y_tick:,}",
        size=11,
        va="center",
        ha="right",
        transform=axs[0].transAxes,
        color='#555555'
    )
    # Add small tick mark
    axs[0].axhline(
        y=y_tick / max_year_value,
        xmin=-0.20,
        xmax=-0.08,
        clip_on=False,
        color="#333333",
        linewidth=1.2,
    )

# Add vertical Y-axis line
axs[0].axvline(x=-0.018, ymin=0, ymax=1.05, clip_on=False,
               color="#333333", linewidth=1.5)

# Add Y-axis label
axs[0].text(
    x=-0.70,
    y=0.5,
    s='Million tonnes CO₂',
    rotation=90,
    va='center',
    ha='center',
    fontsize=12,
    color='#555555',
    fontweight='600',
    transform=axs[0].transAxes
)

# Add main title and subtitle
fig.text(0.5, 0.94, 'Global CO₂ Emissions by Sector',
         ha='center', fontsize=28, fontweight='bold', color='#2C3E50')

fig.text(0.5, 0.88, 'Million tonnes of CO₂ | Evolution from 2015 to 2024',
         ha='center', fontsize=15, color='#7F8C8D')

# Create and add improved manual legend
legend_elements = []
for i, sector in enumerate(sector_order):
    legend_elements.append(
        mpatches.Patch(facecolor=colors[i], edgecolor='white',
                       linewidth=1.5, label=sector)
    )

fig.legend(handles=legend_elements,
           loc='lower center', ncol=4, frameon=False,
           fontsize=12, bbox_to_anchor=(0.5, 0.02),
           columnspacing=3, handlelength=2, handletextpad=1)

# Save the final plot
plt.savefig('../Graphs/co2_sectores_waffle.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none', pad_inches=0.4)

# Show the figure
plt.show()

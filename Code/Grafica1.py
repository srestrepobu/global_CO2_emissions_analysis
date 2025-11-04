# -------------------------------------------------------------
# IMPORT LIBRARIES
# -------------------------------------------------------------
import pandas as pd                    # Data manipulation and analysis
import matplotlib.pyplot as plt         # Plotting library
import matplotlib.animation as animation # For creating animations
from matplotlib.animation import FuncAnimation # Main function for frame-by-frame animation
import numpy as np                      # Numerical operations

# -------------------------------------------------------------
# LOAD AND PREPARE DATA
# -------------------------------------------------------------

# Load Excel file (adjust path if necessary)
archivo = '../Datos/EDGAR_2025_GHG_booklet_2025_fossilCO2only.xlsx'
df = pd.read_excel(archivo, sheet_name='fossil_CO2_totals_by_country')

# Select the global total CO₂ emissions row
# Note: row 215 in Excel corresponds to index 213 in pandas (0-based indexing)
fila_co2_global = df.iloc[213]

# Identify year columns (numeric or string digits)
columnas_años = [col for col in df.columns if isinstance(col, (int, float)) or (isinstance(col, str) and col.isdigit())]

# Extract year and CO₂ emission values
años = [int(col) for col in columnas_años]
valores_co2 = [fila_co2_global[col] for col in columnas_años]

# Create a clean DataFrame for animation
df_animation = pd.DataFrame({
    'Año': años,
    'CO2': valores_co2
})

# Sort by year to ensure chronological order
df_animation = df_animation.sort_values('Año').reset_index(drop=True)

# -------------------------------------------------------------
# DEFINE HISTORICAL EVENTS
# -------------------------------------------------------------
# Each event includes its year range and label to be displayed during animation
events = [
    {'year': 1945, 'year_start': 1945, 'year_end': 1960, 'text': 'End of World War II'},
    {'year': 1973, 'year_start': 1973, 'year_end': 1985, 'text': 'Oil Crisis'},
    {'year': 1991, 'year_start': 1991, 'year_end': 2003, 'text': 'End of Cold War'},
    {'year': 1997, 'year_start': 1997, 'year_end': 2009, 'text': 'Kyoto Protocol'},
    {'year': 2001, 'year_start': 2001, 'year_end': 2013, 'text': 'China joins the WTO'},
    {'year': 2015, 'year_start': 2015, 'year_end': 2030, 'text': 'Paris Agreement'},
]

# -------------------------------------------------------------
# FIGURE AND STYLE SETUP
# -------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 8))   # Create a large figure
fig.patch.set_facecolor('white')          # Set white background for figure
ax.set_facecolor('white')                 # White background for plot area

# Minimalistic design: remove top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#333333')
ax.spines['bottom'].set_color('#333333')
ax.tick_params(colors='#333333', which='both', labelsize=10)

# -------------------------------------------------------------
# INITIAL PLOT ELEMENTS (updated frame-by-frame)
# -------------------------------------------------------------

line, = ax.plot([], [], color='#69b3a2', linewidth=3)  # Main CO₂ line
end_point, = ax.plot([], [], 'o', color='#69b3a2', markersize=10)  # Moving endpoint

# Vertical line and text for historical events
event_vline = ax.axvline(x=0, color='#e74c3c', linestyle='--', linewidth=2, alpha=0)
event_text = ax.text(0.5, 0.94, '', transform=ax.transAxes,
                     fontsize=22, fontweight='bold', color='#e74c3c',
                     ha='center', va='top', alpha=0,
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='white',
                               edgecolor='#e74c3c', linewidth=2, alpha=0))
event_year_text = ax.text(0.5, 0.85, '', transform=ax.transAxes,
                          fontsize=0, color='#555555',
                          ha='center', va='top', alpha=0)

# Text showing the current CO₂ value at the end of the line
value_text = ax.text(0, 0, '', fontsize=12, fontweight='bold',
                     color='#333333', ha='left', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                               edgecolor='#69b3a2', linewidth=1.5))

# Large year label displayed in the corner
current_year_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                            fontsize=32, fontweight='bold', color='#aaaaaa',
                            ha='left', va='top', alpha=0.5)

# -------------------------------------------------------------
# AXES AND STYLE CONFIGURATION
# -------------------------------------------------------------

ax.set_xlim(df_animation['Año'].min(), df_animation['Año'].max())
y_min = df_animation['CO2'].min()
y_max = df_animation['CO2'].max()
y_range = y_max - y_min
ax.set_ylim(y_min - y_range * 0.05, y_max + y_range * 0.15)

ax.set_xlabel('Year', fontsize=13, color='#333333', fontweight='bold')
ax.set_ylabel('Global CO₂ Emissions (million tonnes)',
              fontsize=13, color='#333333', fontweight='bold')
ax.set_title('Global CO₂ Emission Trends Over Time',
             fontsize=18, color='#333333', fontweight='bold', pad=20)

# Add a subtle grid
ax.grid(True, alpha=0.3, color='#cccccc', linestyle='-', linewidth=0.5)

# -------------------------------------------------------------
# ANIMATION FUNCTIONS
# -------------------------------------------------------------

def init():
    """Initialize the animation with empty elements."""
    line.set_data([], [])
    end_point.set_data([], [])
    event_text.set_text('')
    event_text.set_alpha(0)
    event_year_text.set_text('')
    event_year_text.set_alpha(0)
    value_text.set_text('')
    value_text.set_alpha(0)
    current_year_text.set_text('')
    event_vline.set_alpha(0)
    event_text.get_bbox_patch().set_alpha(0)
    return line, end_point, event_text, event_year_text, value_text, current_year_text, event_vline


def animate(frame):
    """Update all graphical elements for each animation frame."""
    # Progressive line update
    x_data = df_animation['Año'][:frame + 1]
    y_data = df_animation['CO2'][:frame + 1]
    line.set_data(x_data, y_data)

    if frame < len(df_animation):
        current_year = df_animation['Año'].iloc[frame]
        current_value = df_animation['CO2'].iloc[frame]

        # Update endpoint and dynamic text values
        end_point.set_data([current_year], [current_value])
        current_year_text.set_text(f'{int(current_year)}')
        value_text.set_text(f'{current_value:,.0f} Mt')
        value_text.set_position((current_year, current_value))
        value_text.set_alpha(1)

        # Check if a historical event should appear
        event_to_show = None
        for event in events:
            if event['year_start'] <= current_year <= event['year_end']:
                event_to_show = event
                break

        # Display event text with smooth fade in/out
        if event_to_show:
            event_text.set_text(event_to_show['text'])
            event_year_text.set_text(f"Year {event_to_show['year']}")

            # Calculate transparency (alpha) for fade effect
            year_in_range = current_year - event_to_show['year_start']
            year_range = event_to_show['year_end'] - event_to_show['year_start']

            if year_in_range < 5:  # Fade in (first 5 years)
                alpha = year_in_range / 5
            elif year_in_range > year_range - 5:  # Fade out (last 5 years)
                alpha = (event_to_show['year_end'] - current_year) / 5
            else:
                alpha = 1.0  # Fully visible

            # Apply transparency to text and vertical line
            alpha = min(1.0, max(0.0, alpha))
            event_text.set_alpha(alpha)
            event_year_text.set_alpha(alpha)
            event_text.get_bbox_patch().set_alpha(alpha * 0.9)
            event_vline.set_xdata([event_to_show['year'], event_to_show['year']])
            event_vline.set_alpha(alpha * 0.6)
        else:
            # Hide event elements when not active
            event_text.set_alpha(0)
            event_year_text.set_alpha(0)
            event_text.get_bbox_patch().set_alpha(0)
            event_vline.set_alpha(0)

    return line, end_point, event_text, event_year_text, value_text, current_year_text, event_vline

# -------------------------------------------------------------
# CREATE AND SAVE ANIMATION
# -------------------------------------------------------------

frames = len(df_animation)  # Total frames (one per year)
anim = FuncAnimation(fig, animate, init_func=init, frames=frames,
                     interval=100, blit=True, repeat=True)

# Save animation as GIF (requires 'pillow' installed)
anim.save('../Graphs/co2_animation.gif', writer='pillow', fps=10, dpi=200)

# Display final animation
plt.tight_layout()
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo Excel
archivo = '../Datos/EDGAR_2025_GHG_booklet_2025_fossilCO2only.xlsx'
df = pd.read_excel(archivo, sheet_name='fossil_CO2_totals_by_country')

# Excluir agregados globales y regionales
exclusions = ['GLOBAL TOTAL', 'EU27', 'INTERNATIONAL SHIPPING', 'INTERNATIONAL AVIATION']
mask = ~df['Country'].str.upper().isin(exclusions)
df_countries = df[mask].copy()

# Extraer las emisiones de CO₂ para el año 2024
year_col = 2024 if 2024 in df_countries.columns else '2024'
df_countries = df_countries[['Country', year_col]].copy()
df_countries.columns = ['Country', 'CO2_2024']

# Filtrar solo valores positivos de emisión
df_countries = df_countries[df_countries['CO2_2024'] > 0].dropna()

# Mapear países a continentes
continent_map = {
    'USA': 'North America', 'CANADA': 'North America', 'MEXICO': 'North America',
    'BRAZIL': 'South America', 'ARGENTINA': 'South America', 'CHILE': 'South America',
    'GERMANY': 'Europe', 'UNITED KINGDOM': 'Europe', 'FRANCE': 'Europe',
    'CHINA': 'Asia', 'INDIA': 'Asia', 'JAPAN': 'Asia',
    'SOUTH AFRICA': 'Africa', 'EGYPT': 'Africa', 'NIGERIA': 'Africa',
    'AUSTRALIA': 'Oceania', 'NEW ZEALAND': 'Oceania'
}

df_countries['Country_Upper'] = df_countries['Country'].str.upper().str.strip()
df_countries['Continent'] = df_countries['Country_Upper'].map(continent_map)

# Filtrar países sin continente asignado
df_countries = df_countries[df_countries['Continent'].notna()].copy()

# Agregar las emisiones de CO₂ por continente
continent_totals = df_countries.groupby('Continent')['CO2_2024'].sum().reset_index()
continent_totals['Percentage'] = (continent_totals['CO2_2024'] / continent_totals['CO2_2024'].sum()) * 100

# Graficar
plt.figure(figsize=(12, 8))

# Crear gráfico de barras apiladas por continente
sns.barplot(x='Continent', y='CO2_2024', data=continent_totals, palette='Set2')

# Añadir etiquetas y título
plt.title('CO₂ Emissions by Continent (2024)', fontsize=18)
plt.xlabel('Continent', fontsize=14)
plt.ylabel('CO₂ Emissions (Million Tonnes)', fontsize=14)

# Mostrar el porcentaje sobre las barras
for i, row in continent_totals.iterrows():
    plt.text(i, row['CO2_2024'] + 50, f"{row['Percentage']:.1f}%", ha='center', fontsize=12)

# Ajustar presentación
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("../Graphs/CO2_Emissions_by_Continent_(2024)", dpi=300, bbox_inches="tight")
# Mostrar el gráfico
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo Excel
input_file_path = '../Datos/life-expectancy-at-birth-vs-co-emissions-per-capita.xlsx'
df = pd.read_excel(input_file_path, sheet_name='life-expectancy-at-birth-vs-co-')

# Filtrar los datos para el año 2023
df_2023 = df[df['Year'] == 2023]

# Seleccionar las columnas de interés
df_2023 = df_2023[['Entity', 'Life expectancy - Sex: all - Age: 0 - Variant: estimates',
                    'Carbon dioxide (CO2) emissions excluding LULUCF per capita (t CO2e/capita)',
                    'World regions according to OWID']]

# Renombrar las columnas para mayor claridad
df_2023 = df_2023.rename(columns={
    'Entity': 'Country',
    'Life expectancy - Sex: all - Age: 0 - Variant: estimates': 'Life expectancy',
    'Carbon dioxide (CO2) emissions excluding LULUCF per capita (t CO2e/capita)': 'CO2 emissions per capita',
    'World regions according to OWID': 'Region'
})

# Eliminar filas con valores nulos en las columnas de interés
df_2023 = df_2023.dropna(subset=['Life expectancy', 'CO2 emissions per capita'])

#
df_2023['Life expectancy'] = df_2023['Life expectancy']

# Crear una paleta de colores para las regiones
region_colors = sns.color_palette("Set1", len(df_2023['Region'].unique()))

# Crear el gráfico de dispersión
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")

# Graficar cada región con un color distinto
for i, region in enumerate(df_2023['Region'].unique()):
    region_data = df_2023[df_2023['Region'] == region]
    plt.scatter(region_data['CO2 emissions per capita'], region_data['Life expectancy'],
                label=region, color=region_colors[i], alpha=0.7, s=100)

# Ajustes del gráfico
plt.xscale('log')  # Escala logarítmica para el eje X (emisiones de CO2)
plt.title('Life Expectancy vs CO2 Emissions per Capita (2023)', fontsize=16)
plt.xlabel('CO2 emissions per capita (tonnes)', fontsize=12)
plt.ylabel('Life expectancy at birth (years)', fontsize=12)
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')

# Mostrar el gráfico
plt.tight_layout()
plt.savefig("../Graphs/Life_Expectancy_vs_CO2_Emissions_per_Capita_(2023).png", dpi=300, bbox_inches="tight")
plt.show()

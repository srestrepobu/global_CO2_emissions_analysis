import pandas as pd
import plotly.express as px

# Definir la ruta de entrada del archivo Excel
input_file_path = '../Datos/life-expectancy-at-birth-vs-co-emissions-per-capita.xlsx'

# Cargar el archivo Excel
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

# Eliminar filas con valores nulos o vacíos en la columna 'Region'
df_2023_cleaned = df_2023[df_2023['Region'].notna() & (df_2023['Region'] != '')]

# Crear la gráfica de dispersión interactiva
fig = px.scatter(df_2023_cleaned,
                 x='CO2 emissions per capita',
                 y='Life expectancy',
                 color='Region',
                 hover_name='Country',
                 log_x=True,  # Logarithmic scale for CO2 emissions
                 title="Life Expectancy vs CO2 Emissions per Capita (2023)",
                 labels={'CO2 emissions per capita': 'CO2 emissions per capita (tonnes per capita; plotted on a logarithmic axis)',
                         'Life expectancy': 'Life expectancy at birth (years)'})

# Guardar la gráfica como un archivo HTML interactivo en la misma ruta donde se ejecuta el código
output_file_path = '../Graphs/life_expectancy_vs_co2_2023_cleaned.html'
fig.write_html(output_file_path)
fig.show()

import pandas as pd
import plotly.express as px

# Leer datos
archivo = '../Datos/EDGAR_2025_GHG_booklet_2025_fossilCO2only.xlsx'
df = pd.read_excel(archivo, sheet_name='fossil_CO2_totals_by_country')


# Filtrar exclusiones
exclusiones = ['GLOBAL TOTAL', 'EU27', 'INTERNATIONAL SHIPPING', 'INTERNATIONAL AVIATION']
mask = ~df['Country'].str.upper().isin(exclusiones)
df_paises = df[mask].copy()

# Extraer 2024
year_col = 2024 if 2024 in df_paises.columns else '2024'
df_paises = df_paises[['Country', year_col]].copy()
df_paises.columns = ['Country', 'CO2_2024']
df_paises = df_paises[df_paises['CO2_2024'] > 0].dropna()

# Mapeo de países a continentes
continent_map = {
    # América del Norte
    'USA': 'North America',
    'UNITED STATES': 'North America',
    'UNITED STATES OF AMERICA': 'North America',
    'CANADA': 'North America',
    'MEXICO': 'North America',
    'GUATEMALA': 'North America', 'HONDURAS': 'North America', 'EL SALVADOR': 'North America',
    'NICARAGUA': 'North America', 'COSTA RICA': 'North America', 'PANAMA': 'North America',
    'CUBA': 'North America', 'JAMAICA': 'North America', 'HAITI': 'North America',
    'DOMINICAN REPUBLIC': 'North America', 'TRINIDAD AND TOBAGO': 'North America',

    # América del Sur
    'BRAZIL': 'South America', 'ARGENTINA': 'South America', 'CHILE': 'South America',
    'COLOMBIA': 'South America', 'VENEZUELA': 'South America',
    'VENEZUELA (BOLIVARIAN REPUBLIC OF)': 'South America',
    'PERU': 'South America', 'ECUADOR': 'South America', 'BOLIVIA': 'South America',
    'BOLIVIA (PLURINATIONAL STATE OF)': 'South America',
    'PARAGUAY': 'South America', 'URUGUAY': 'South America', 'SURINAME': 'South America',
    'GUYANA': 'South America',

    # Europa
    'GERMANY': 'Europe', 'UNITED KINGDOM': 'Europe', 'FRANCE': 'Europe', 'ITALY': 'Europe',
    'SPAIN': 'Europe', 'POLAND': 'Europe', 'NETHERLANDS': 'Europe', 'BELGIUM': 'Europe',
    'GREECE': 'Europe', 'PORTUGAL': 'Europe', 'AUSTRIA': 'Europe', 'SWEDEN': 'Europe',
    'FINLAND': 'Europe', 'DENMARK': 'Europe', 'NORWAY': 'Europe', 'IRELAND': 'Europe',
    'SWITZERLAND': 'Europe', 'ROMANIA': 'Europe', 'CZECHIA': 'Europe',
    'CZECH REPUBLIC': 'Europe', 'HUNGARY': 'Europe', 'SLOVAKIA': 'Europe',
    'BULGARIA': 'Europe', 'CROATIA': 'Europe', 'SERBIA': 'Europe', 'SLOVENIA': 'Europe',
    'LITHUANIA': 'Europe', 'LATVIA': 'Europe', 'ESTONIA': 'Europe', 'ICELAND': 'Europe',
    'LUXEMBOURG': 'Europe', 'MALTA': 'Europe', 'CYPRUS': 'Europe',
    'ALBANIA': 'Europe', 'NORTH MACEDONIA': 'Europe', 'MONTENEGRO': 'Europe',
    'BOSNIA AND HERZEGOVINA': 'Europe', 'UKRAINE': 'Europe', 'BELARUS': 'Europe',
    'MOLDOVA': 'Europe',

    # Asia
    'CHINA': 'Asia', 'CHINA (MAINLAND)': 'Asia', 'INDIA': 'Asia', 'JAPAN': 'Asia',
    'KOREA (SOUTH)': 'Asia', 'INDONESIA': 'Asia', 'SAUDI ARABIA': 'Asia',
    'IRAN': 'Asia', 'IRAN (ISLAMIC REPUBLIC OF)': 'Asia', 'THAILAND': 'Asia',
    'MALAYSIA': 'Asia', 'SINGAPORE': 'Asia', 'PHILIPPINES': 'Asia', 'VIETNAM': 'Asia',
    'VIET NAM': 'Asia', 'PAKISTAN': 'Asia', 'BANGLADESH': 'Asia', 'IRAQ': 'Asia',
    'UNITED ARAB EMIRATES': 'Asia', 'QATAR': 'Asia', 'KUWAIT': 'Asia', 'OMAN': 'Asia',
    'ISRAEL': 'Asia', 'LEBANON': 'Asia', 'JORDAN': 'Asia', 'SYRIA': 'Asia',
    'YEMEN': 'Asia', 'SRI LANKA': 'Asia', 'MYANMAR': 'Asia', 'CAMBODIA': 'Asia',
    'LAOS': 'Asia', 'NEPAL': 'Asia', 'AFGHANISTAN': 'Asia', 'MONGOLIA': 'Asia',
    'KOREA (NORTH)': 'Asia', 'TAIWAN': 'Asia', 'BAHRAIN': 'Asia', 'BRUNEI': 'Asia',
    'MALDIVES': 'Asia', 'BHUTAN': 'Asia', 'TIMOR-LESTE': 'Asia',
    'AZERBAIJAN': 'Asia', 'ARMENIA': 'Asia', 'GEORGIA': 'Asia',
    'KAZAKHSTAN': 'Asia', 'UZBEKISTAN': 'Asia', 'TURKMENISTAN': 'Asia',
    'KYRGYZSTAN': 'Asia', 'TAJIKISTAN': 'Asia',

    # África
    'SOUTH AFRICA': 'Africa', 'EGYPT': 'Africa', 'NIGERIA': 'Africa', 'ALGERIA': 'Africa',
    'MOROCCO': 'Africa', 'LIBYA': 'Africa', 'TUNISIA': 'Africa', 'KENYA': 'Africa',
    'ETHIOPIA': 'Africa', 'GHANA': 'Africa', 'ANGOLA': 'Africa', 'SUDAN': 'Africa',
    'TANZANIA': 'Africa', 'TANZANIA (UNITED REPUBLIC OF)': 'Africa',
    'CAMEROON': 'Africa', 'UGANDA': 'Africa', 'ZIMBABWE': 'Africa', 'ZAMBIA': 'Africa',
    'SENEGAL': 'Africa', 'MOZAMBIQUE': 'Africa', 'MADAGASCAR': 'Africa',
    'CÔTE D\'IVOIRE': 'Africa', 'MALI': 'Africa', 'BURKINA FASO': 'Africa',
    'NIGER': 'Africa', 'MALAWI': 'Africa', 'GUINEA': 'Africa', 'RWANDA': 'Africa',
    'BENIN': 'Africa', 'BURUNDI': 'Africa', 'CHAD': 'Africa', 'SOMALIA': 'Africa',
    'CONGO': 'Africa', 'CONGO (DEMOCRATIC REPUBLIC OF THE)': 'Africa',
    'GABON': 'Africa', 'MAURITANIA': 'Africa', 'NAMIBIA': 'Africa', 'BOTSWANA': 'Africa',
    'MAURITIUS': 'Africa', 'TOGO': 'Africa', 'SIERRA LEONE': 'Africa', 'LIBERIA': 'Africa',

    # Oceanía
    'AUSTRALIA': 'Oceania', 'NEW ZEALAND': 'Oceania', 'PAPUA NEW GUINEA': 'Oceania',
    'FIJI': 'Oceania',

    # Rusia (Europa/Asia - lo ponemos en Europa por convención)
    'RUSSIA': 'Europe', 'RUSSIAN FEDERATION': 'Europe', 'TURKEY': 'Europe'
}

# Asignar continentes
df_paises['Country_Upper'] = df_paises['Country'].str.upper().str.strip()
df_paises['Continent'] = df_paises['Country_Upper'].map(continent_map)

# Filtrar solo países con continente asignado
df_paises = df_paises[df_paises['Continent'].notna()].copy()


# Calcular totales y porcentajes
total_global = df_paises['CO2_2024'].sum()
df_paises['Percentage'] = (df_paises['CO2_2024'] / total_global) * 100

# Calcular totales por continente
continent_totals = df_paises.groupby('Continent')['CO2_2024'].sum().reset_index()
continent_totals['Cont_Percentage'] = (continent_totals['CO2_2024'] / total_global) * 100

print("\nEmisiones por continente:")
print(continent_totals.sort_values('CO2_2024', ascending=False))

# Crear etiquetas personalizadas
df_paises['Label'] = df_paises.apply(
    lambda x: f"<b>{x['Country']}</b><br>{x['CO2_2024']:.1f} billion t<br>{x['Percentage']:.1f}%",
    axis=1
)

# Colores por continente
continent_colors = {
    'North America': '#2ecc71',  # Verde
    'South America': '#27ae60',  # Verde oscuro
    'Europe': '#f39c12',  # Naranja
    'Asia': '#e74c3c',  # Rojo
    'Africa': '#3498db',  # Azul
    'Oceania': '#9b59b6'  # Morado
}

df_paises['Color'] = df_paises['Continent'].map(continent_colors)

# Crear treemap
fig = px.treemap(
    df_paises,
    path=['Continent', 'Country'],
    values='CO2_2024',
    color='Continent',
    color_discrete_map=continent_colors,
    custom_data=['CO2_2024', 'Percentage']
)

# Personalizar hover y texto
fig.update_traces(
    textposition='middle center',
    textfont=dict(size=12, color='white', family='Arial'),
    hovertemplate='<b>%{label}</b><br>CO₂: %{customdata[0]:.1f} Mt<br>%{customdata[1]:.2f}% global<extra></extra>',
    marker=dict(line=dict(width=2, color='white'))
)

# Layout
fig.update_layout(
    title={
        'text': 'Who has contributed most to global CO₂ emissions?<br><sub>Carbon dioxide emissions in 2024 (million tonnes)</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 28, 'color': '#2C3E50', 'family': 'Arial'}
    },
    width=1400,
    height=800,
    paper_bgcolor='white',
    font=dict(family='Arial', size=14)
)

# Guardar
fig.write_html('../Graphs/co2_treemap_2024.html')

fig.show()


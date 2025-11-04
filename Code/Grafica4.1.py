import pandas as pd
import plotly.express as px

# === Load and preprocess data ===

# Path to the Excel file containing CO₂ emission data
archivo = '../Datos/EDGAR_2025_GHG_booklet_2025_fossilCO2only.xlsx'

# Read the sheet containing fossil CO₂ totals by country
# Requires the 'openpyxl' library to read .xlsx files.
# If you get the error:
#   ImportError: Missing optional dependency 'openpyxl'
# fix it by running: pip install openpyxl
df = pd.read_excel(archivo, sheet_name='fossil_CO2_totals_by_country')

# === Filter out non-country entries ===
# Exclude global and regional aggregates that could distort the results.
exclusions = ['GLOBAL TOTAL', 'EU27', 'INTERNATIONAL SHIPPING', 'INTERNATIONAL AVIATION']
mask = ~df['Country'].str.upper().isin(exclusions)
df_countries = df[mask].copy()

# === Extract CO₂ emissions for the year 2024 ===
# Some datasets may store column names as strings ("2024") or integers (2024).
year_col = 2024 if 2024 in df_countries.columns else '2024'
df_countries = df_countries[['Country', year_col]].copy()
df_countries.columns = ['Country', 'CO2_2024']

# Keep only positive emission values
df_countries = df_countries[df_countries['CO2_2024'] > 0].dropna()

# === Map countries to continents ===
# This dictionary allows grouping countries by continent for visualization.
continent_map = {
    # North America
    'USA': 'North America', 'UNITED STATES': 'North America', 'UNITED STATES OF AMERICA': 'North America',
    'CANADA': 'North America', 'MEXICO': 'North America',
    'GUATEMALA': 'North America', 'HONDURAS': 'North America', 'EL SALVADOR': 'North America',
    'NICARAGUA': 'North America', 'COSTA RICA': 'North America', 'PANAMA': 'North America',
    'CUBA': 'North America', 'JAMAICA': 'North America', 'HAITI': 'North America',
    'DOMINICAN REPUBLIC': 'North America', 'TRINIDAD AND TOBAGO': 'North America',

    # South America
    'BRAZIL': 'South America', 'ARGENTINA': 'South America', 'CHILE': 'South America',
    'COLOMBIA': 'South America', 'VENEZUELA': 'South America',
    'VENEZUELA (BOLIVARIAN REPUBLIC OF)': 'South America',
    'PERU': 'South America', 'ECUADOR': 'South America', 'BOLIVIA': 'South America',
    'BOLIVIA (PLURINATIONAL STATE OF)': 'South America',
    'PARAGUAY': 'South America', 'URUGUAY': 'South America', 'SURINAME': 'South America',
    'GUYANA': 'South America',

    # Europe
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

    # Africa
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

    # Oceania
    'AUSTRALIA': 'Oceania', 'NEW ZEALAND': 'Oceania', 'PAPUA NEW GUINEA': 'Oceania',
    'FIJI': 'Oceania',

    # Russia (classified as Europe for simplicity)
    'RUSSIA': 'Europe', 'RUSSIAN FEDERATION': 'Europe', 'TURKEY': 'Europe'
}

# Convert country names to uppercase and map to continents
df_countries['Country_Upper'] = df_countries['Country'].str.upper().str.strip()
df_countries['Continent'] = df_countries['Country_Upper'].map(continent_map)

# Debug: identify any countries missing a continent assignment
missing = df_countries[df_countries['Continent'].isna()]
if len(missing) > 0:
    print("\nCountries without continent mapping:")
    print(missing[['Country', 'Country_Upper', 'CO2_2024']].head(20))

# Keep only countries with assigned continents
df_countries = df_countries[df_countries['Continent'].notna()].copy()

# === Summary statistics ===
print(f"\nProcessed countries: {len(df_countries)}")
print("\nTop 10 emitters:")
print(df_countries.nlargest(10, 'CO2_2024')[['Country', 'Continent', 'CO2_2024']])

# Compute global total and share per country
total_global = df_countries['CO2_2024'].sum()
df_countries['Percentage'] = (df_countries['CO2_2024'] / total_global) * 100

# Aggregate by continent
continent_totals = df_countries.groupby('Continent')['CO2_2024'].sum().reset_index()
continent_totals['Cont_Percentage'] = (continent_totals['CO2_2024'] / total_global) * 100


# === Label customization for better treemap readability ===
df_countries['Label'] = df_countries.apply(
    lambda x: f"{x['Country']}<br>{x['CO2_2024']:.0f} Mt<br>{x['Percentage']:.1f}%"
    if x['Percentage'] > 1.0 else
    f"{x['Country']}" if x['Percentage'] > 0.3 else "",
    axis=1
)

# === Color mapping for continents ===
continent_colors = {
    'North America': '#2ecc71',  # Green
    'South America': '#27ae60',  # Dark green
    'Europe': '#f39c12',         # Orange
    'Asia': '#e74c3c',           # Red
    'Africa': '#3498db',         # Blue
    'Oceania': '#9b59b6'         # Purple
}

df_countries['Color'] = df_countries['Continent'].map(continent_colors)

# === Build the Treemap using Plotly Express ===
fig = px.treemap(
    df_countries,
    path=['Continent', 'Country'],
    values='CO2_2024',
    color='Continent',
    color_discrete_map=continent_colors,
    custom_data=['CO2_2024', 'Percentage', 'Country']
)

# === Customize treemap text and hover info ===
fig.update_traces(
    textposition='middle center',
    texttemplate='%{customdata[2]}<br><b>%{customdata[0]:.0f} Mt</b><br>%{customdata[1]:.1f}%',
    textfont=dict(size=11, color='white', family='Arial, sans-serif'),
    hovertemplate='<b>%{customdata[2]}</b><br>CO₂: %{customdata[0]:,.0f} Mt<br>%{customdata[1]:.2f}% of global emissions<extra></extra>',
    marker=dict(
        line=dict(width=2, color='white'),
        pad=dict(t=30, l=5, r=5, b=5)
    )
)

# === Layout settings for appearance and readability ===
fig.update_layout(
    title={
        'text': 'Who has contributed most to global CO₂ emissions?<br><sub>CO₂ emissions in 2024 (million tonnes)</sub>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 28, 'color': '#2C3E50', 'family': 'Arial'}
    },
    width=1400,
    height=800,
    paper_bgcolor='white',
    font=dict(family='Arial', size=14)
)

# === Export interactive chart as HTML ===
fig.write_html('../Graphs/co2_treemap_2024_v1.html')

# Show in browser / interactive window
fig.show()

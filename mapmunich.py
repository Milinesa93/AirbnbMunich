import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import requests
import json
import geopy.distance
import geopandas as gpd
from shapely.geometry import Point, Polygon
import streamlit as st
import streamlit_folium as sf
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from folium import IFrame
import streamlit.components.v1 as components
import yfinance as yf
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import tempfile
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.colors as mcolors


# Leer el archivo CSV
file_path = 'top10munichairbnb.csv'
top10munich_df = pd.read_csv(file_path)

file_pathprop = 'properties.csv'
properties_df = pd.read_csv(file_pathprop)

st.image('castillomunich.png', width=700)

# Titulo de la página que aparece
st.markdown("""
    <style>
    .fade-in {
        animation: fadeIn 4s ease-in-out;
    }

    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    .title-container {
        background-color:none;
        padding:30px;
        border-radius:20px;
        border:2px solid #E47302 ;
        text-align:center;
    }

    .title-text {
        color:white;
        font-size:2em; /* Modified font size */
    }
    </style>
    <div class="title-container fade-in">
        <h1 class="title-text">Análisis de Inversión en Munich: <br><br> Zona Theresienwiese <br><br> Asesora: Milagros Vidal</h1>
    </div>
    <br><br> 
    """, unsafe_allow_html=True)

#info sobre el oktoberfest: nivel de ocupacion y cantidad de gente que va al año aprox

st.markdown("<h1 style='text-align: center;'>Oktoberfest en Munich</h1>", unsafe_allow_html=True)


kagledf = pd.read_csv('oktoberfest.csv')

# Filtrar los datos para los últimos 5 años
last_5_years_df = kagledf.sort_values(by='year', ascending=False).head(5)

# grafico para ver ultimos 5 años
fig, ax = plt.subplots(figsize=(10, 6))


ax.plot(last_5_years_df['year'], last_5_years_df['guests_total'], marker='o', color='#66b', linestyle='-', linewidth=2, markersize=8)
ax.set_xlabel('Año', color='white')
ax.set_ylabel('Total de Invitados (Millones)', color='white')
ax.set_title('Total de visitantes al Oktoberfest en los Últimos 5 Años', color='white')
ax.invert_xaxis()  

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.yaxis.grid(False, linestyle='-', alpha=0.7, color='white')
ax.xaxis.grid(False)
ax.invert_xaxis()  

ax.set_facecolor('none')
fig.patch.set_facecolor('none')

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
plt.xticks(rotation=45, color='white')
plt.yticks(rotation=0, color='white')

# grafico de los ultimos 5 años del oktoberfest
st.pyplot(fig)

# Data de meses y tasas de ocupación
months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Agos', 'Sep', 'Oct', 'Nov', 'Dic']
occupancy_rates = [39, 40, 42, 45, 50, 55, 60, 65, 70, 68, 50, 45]

data = pd.DataFrame({
    'Month': months,
    'Occupancy Rate (%)': occupancy_rates
})

fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')
ax.plot(data['Month'], data['Occupancy Rate (%)'], marker='o', linestyle='-', color='pink')

oktoberfest_start = 'Sep'
oktoberfest_end = 'Oct'
ax.axvline(x=oktoberfest_start, color='yellow', linestyle='--', linewidth=2, label='Oktoberfest comienzo')
ax.axvline(x=oktoberfest_end, color='yellow', linestyle='--', linewidth=2, label='Oktoberfest fin')

ax.legend() # leyenda de los meses de Oktoberfest

ax.set_title('Ocupación anual', color='white')
ax.set_xlabel('Mes', color='white')
ax.set_ylabel('Ocupación (%)', color='white')

ax.tick_params(colors='white')

fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['right'].set_color('white')
ax.yaxis.grid(False, linestyle='-', alpha=0.7, color='white')


st.pyplot(fig)

# canalaes que se reservan alojamiento en Munich

# Datos para el gráfico de barra
labels = ['Airbnb', 'Vrbo', 'Ambos']
sizes = [8388, 82, 171]
colors = ['#66b', '#f9c', '#6cf']

# Calcular porcentajes
total = sum(sizes)
percentages = [(size / total) * 100 for size in sizes]

# Crear gráfico de barra
fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')
ax.bar(labels, sizes, color=colors)

# Agregar etiquetas de datos
for i, v in enumerate(sizes):
    ax.text(i, v + 50, f"{v} ({percentages[i]:.2f}%)", color='white', ha='center')

# Configuraciones adicionales
ax.set_title('Distribución de canales de reservas', color='white')
ax.set_xlabel('Tipo de Alojamiento', color='white')
ax.set_ylabel('Cantidad', color='white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['right'].set_color('white')
ax.yaxis.grid(False)
ax.xaxis.grid(False)
ax.tick_params(colors='white')

fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)
# Mostrar gráfico
st.pyplot(fig)

# tabla top10 de los Airbnb en Munich
st.markdown("<h1 style='text-align: center;'>Top 10 de Airbnb en Munich</h1>", unsafe_allow_html=True)
st.dataframe(top10munich_df[['neighbourhood', 'room_type', 'price_perday', 'review_scores_location', 'accomodates']])

# Crear mapa centrado en Theresienwiese-Octokerfest
m = folium.Map(location=[48.13583263039702, 11.545248777231926], zoom_start=12)

# popup para Theresienwiese al ser el punto de interes del cliente
popup_html = """
<div style="font-family: Arial; color: black; max-width: 300px;">
    <strong>Barrio Octokerfest:</strong> Theresienwiese
</div>
"""
popup = folium.Popup(popup_html, max_width=300)

folium.Marker([48.13583263039702, 11.545248777231926], popup=popup).add_to(m)


# Circulo de 2 kilómetros de radio alrededor de Theresienwiese para cuales airbnb se encuentran cerca
folium.Circle(
    location=[48.13583263039702, 11.545248777231926],
    radius=2000,  # Radio en metros
    color='darkviolet',
    fill=True,
    fill_color='violet',
    fill_opacity=0.2
).add_to(m)

#icono de airbnb para que se vea mas pro
icon_path = 'logoairbnb.png'

# icono airbnb customizado
for idx, row in top10munich_df.iterrows():
    icon = folium.CustomIcon(icon_path, icon_size=(45, 35))  # Ajusta el tamaño del icono según sea necesario
    
    # Crear popup con HTML y CSS para mejor visualización
    popup_html = f"""
    <div style="font-family: Arial; color: black; max-width: 300px;">
        <strong>Neighbourhood:</strong> {row['neighbourhood']}<br><br>
        <strong>Room Type:</strong> {row['room_type']}<br><br>
        <strong>Price per day:</strong> ${row['price_perday']}<br><br>
        <strong>Review Scores Location:</strong> {row['review_scores_location']}<br><br>
        {'<strong>Accomodates:</strong> ' + str(row['accomodates'])}
    </div>
    """
    popup = folium.Popup(popup_html, max_width=300)
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup,
        icon=icon
    ).add_to(m)
    
    
# mapa en Streamlit
folium_static(m)

#### HASTA ACA EL MAPA DE AIRBNB

st.markdown("<h1 style='text-align: center;'>Propiedades en Munich</h1>", unsafe_allow_html=True)

# Leer el archivo de propiedades
file_pathprop = 'properties.csv'
properties_df = pd.read_csv(file_pathprop)

# Mostrar tabla de propiedades
st.dataframe(properties_df)


st.markdown("<h1 style='text-align: center;'>Análisis de Rentabilidad de Propiedades en Munich</h1>", unsafe_allow_html=True)

# Análisis de Propiedades
properties_df['dimension'] = properties_df['dimension'].str.replace('m²', '').astype(int)

# ingreso anual por renta
properties_df['annual_rent_income'] = properties_df['price_rent'] * 12

# Calcular ROI como ingreso anual por renta dividido por pricepop
properties_df['roi'] = properties_df['annual_rent_income'] / properties_df['pricepop']

# período de recuperación del capital (años para recuperar la inversión)
properties_df['payback_period'] = properties_df['pricepop'] / properties_df['annual_rent_income']

# Gráfico de Rentabilidad Anual (ROI)
fig_roi = px.bar(
    properties_df.sort_values(by='roi', ascending=False),
    x='id',
    y='roi',
    labels={'roi': 'ROI (%)', 'id': 'Propiedad'},
    title='Rentabilidad Anual (ROI) por Propiedad',
    color='roi',
    color_continuous_scale=px.colors.sequential.Teal
)

st.write("Retorno Sobre la Inversión. Es una métrica usada para saber cuánto se ganó a través de sus inversiones.")

# Gráfico de Período de Recuperación del Capital
fig_payback = px.bar(
    properties_df.sort_values(by='payback_period', ascending=True),
    x='id',
    y='payback_period',
    labels={'payback_period': 'Período de Recuperación (meses)', 'id': 'Propiedad'},
    title='Período de Recuperación del Capital por Propiedad',
    color='payback_period',
    color_continuous_scale=px.colors.sequential.Sunset
)

# Línea de tiempo de recuperación de capital y ganancias acumuladas
fig_timeline = go.Figure()


for index, row in properties_df.iterrows():
    years = list(range(1, 11))
    capital_recovered = [min(row['pricepop'], year * row['annual_rent_income']) for year in years]
    gains = [max(0, year * row['annual_rent_income'] - row['pricepop']) for year in years]
    
    fig_timeline.add_trace(go.Scatter(
        x=years,
        y=capital_recovered,
        mode='lines+markers',
        name=f"{row['id']} - Recuperación de Capital"
    ))
    
    fig_timeline.add_trace(go.Scatter(
        x=years,
        y=gains,
        mode='lines+markers',
        name=f"{row['id']} - Ganancias"
    ))

fig_timeline.update_layout(
    title='Línea de Tiempo de Recuperación de Capital y Ganancias Acumuladas',
    xaxis_title='Años',
    yaxis_title='Dinero (€)',
    legend_title='Propiedades',
    template='plotly_white'
)


st.plotly_chart(fig_roi)
st.plotly_chart(fig_payback)
st.plotly_chart(fig_timeline)

# Análisis y Conclusión
st.header("Recomendaciones y Conclusión")
st.markdown("""
**Recomendaciones al Comprador:**
1. **Rentabilidad Anual (ROI):** 
   - La propiedad **"Ludwigsvorstadt Isar.26m²"** presenta la mayor rentabilidad anual con un ROI del 45.28%. Esto significa que, en comparación con otras propiedades, esta generará mayores ingresos anuales respecto a su precio de compra.
   
2. **Período de Recuperación del Capital:**
   - La misma propiedad **"Ludwigsvorstadt Isar.26m²"** también tiene el menor período de recuperación del capital con aproximadamente en 8 meses. Esto indica que recuperará la inversión inicial más rápido que las otras propiedades.

### Conclusión:
La propiedad **"Ludwigsvorstadt Isar.26m²"** es la mejor opción para invertir y arrendar en Airbnb. Esta propiedad no solo permitirá recuperar el capital invertido más rápidamente, sino que también generará las mejores ganancias anuales en relación con su precio de compra. Por lo tanto, se recomienda invertir en esta propiedad para maximizar las ganancias y recuperar rápidamente la inversión.
""")



st.markdown("<h2 style='text-align: center;'>¡Gracias por su preferencia!</h2>", unsafe_allow_html=True)


# Nota al pie con borde naranja
footer = """
<div style="border:2px solid #E47302; padding: 10px; margin-top: 20px;">
    <p>Contacto: mvidal@muncheninm.de</p>
    <p>Teléfono: +49 89 12345678</p>
    <p>Dirección: Schloss Nymphenburg, 80638 München, Alemania</p>
    <p>Horario de Atención: Lunes a Viernes de 9:00 am a 5:00 pm</p>
    <p>Sitio Web: <a href="https://www.muncheninm.de" target="_blank">München Inmuebles</a></p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)



#recurso de como hacer html y colores: https://htmlcolorcodes.com/es/selector-de-color/
# fuentes utilizadas:
# https://www.kaggle.com/oktoberfest/oktoberfest
#https://app.airdna.co/data/de/30852?tab=performance

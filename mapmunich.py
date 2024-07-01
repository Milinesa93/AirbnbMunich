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
        font-size:3em;
    }
    </style>
    <div class="title-container fade-in">
        <h1 class="title-text">Análisis de Inversión en Munich: <br><br> Zona Theresienwiese</h1>
    </div>
    <br><br> 
    """, unsafe_allow_html=True)

#info sobre el oktoberfest: nivel de ocupacion y cantidad de gente que va al año aprox

st.markdown("<h1 style='text-align: center;'>Oktoberfest en Munich</h1>", unsafe_allow_html=True)


kagledf = pd.read_csv('oktoberfest.csv')

# Filtrar los datos para los últimos 5 años
last_5_years_df = kagledf.sort_values(by='year', ascending=False).head(5)

# Crear el gráfico de línea
fig, ax = plt.subplots(figsize=(10, 6))


ax.plot(last_5_years_df['year'], last_5_years_df['guests_total'], marker='o', color='#66b', linestyle='-', linewidth=2, markersize=8)
ax.set_xlabel('Año', color='white')
ax.set_ylabel('Total de Invitados (Millones)', color='white')
ax.set_title('Total de visitantes al Oktoberfest en los Últimos 5 Años', color='white')
ax.invert_xaxis()  # Invertir el eje x para mostrar el año más reciente a la derecha

# Estilo limpio y minimalista
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.yaxis.grid(False, linestyle='-', alpha=0.7, color='white')
ax.xaxis.grid(False)
ax.invert_xaxis()  

# Cambiar el fondo del gráfico
ax.set_facecolor('none')
fig.patch.set_facecolor('none')


ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
plt.xticks(rotation=45, color='white')
plt.yticks(rotation=0, color='white')

# grafico de los ultimos 5 años del oktoberfest
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
    
    
# Mostrar el mapa en Streamlit
folium_static(m)

#### HASTA ACA EL MAPA DE AIRBNB


# Convertir dimension a valor numérico (quitar 'm²' y convertir a int)
properties_df['dimension'] = properties_df['dimension'].str.replace('m²', '').astype(int)

# Calcular ingreso anual por renta
properties_df['annual_rent_income'] = properties_df['price_rent'] * 12

# Calcular ROI (Return on Investment) como ingreso anual por renta dividido por pricepop
properties_df['roi'] = properties_df['annual_rent_income'] / properties_df['pricepop']

# Calcular período de recuperación del capital (años para recuperar la inversión)
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

# Gráfico de Período de Recuperación del Capital
fig_payback = px.bar(
    properties_df.sort_values(by='payback_period', ascending=True),
    x='id',
    y='payback_period',
    labels={'payback_period': 'Período de Recuperación (años)', 'id': 'Propiedad'},
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

# Mostrar gráficos en Streamlit
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
   - La misma propiedad **"Ludwigsvorstadt Isar.26m²"** también tiene el menor período de recuperación del capital con aproximadamente 0.022 años (casi 8 meses). Esto indica que recuperará la inversión inicial más rápido que las otras propiedades.

### Conclusión:
La propiedad **"Ludwigsvorstadt Isar.26m²"** es la mejor opción para invertir y arrendar en Airbnb. Esta propiedad no solo permitirá recuperar el capital invertido más rápidamente, sino que también generará las mejores ganancias anuales en relación con su precio de compra. Por lo tanto, se recomienda invertir en esta propiedad para maximizar las ganancias y recuperar rápidamente la inversión.
""")


#recurso de como hacer html y colores: https://htmlcolorcodes.com/es/selector-de-color/

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



# Leer el archivo CSV
file_path = 'top10munichairbnb.csv'
top10munich_df = pd.read_csv(file_path)

file_pathprop = 'properties.csv'
properties_df = pd.read_csv(file_pathprop)



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
        background-color:#E47302 ;
        padding:10px;
        border-radius:20px;
        border:2px solid #1E90;
        text-align:center;
    }

    .title-text {
        color:white;
        font-size:3.5em;
    }
    </style>
    <div class="title-container fade-in">
        <h1 class="title-text">Análisis de Inversión en Munich: <br><br> Zona Theresienwiese</h1>
    </div>
    """, unsafe_allow_html=True)



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

# file_pathprop = 'properties.csv'
# properties_df = pd.read_csv(file_pathprop)


# # Calcular el tiempo de recuperación de la inversión
# properties_df['time_to_recover'] = properties_df['pricepop'] / (properties_df['price_rent'] * 12)

# # Calcular las ganancias en 10 años
# properties_df['profit_10_years'] = (properties_df['price_rent'] * 12 * 10) - properties_df['pricepop']

# # Identificar la propiedad con menor tiempo de recuperación y mayor ganancia en 10 años
# min_recovery_time = properties_df.loc[properties_df['time_to_recover'].idxmin()]
# max_profit_10_years = properties_df.loc[properties_df['profit_10_years'].idxmax()]

# # Configurar la página de Streamlit
# st.title("Análisis de Propiedades")

# st.header("Propiedad con menor tiempo de recuperación de la inversión")
# st.write(f"**ID:** {min_recovery_time['id']}")
# st.write(f"**Ubicación:** {min_recovery_time['neighbourhoodMun']}")
# st.write(f"**Habitaciones:** {min_recovery_time['rooms']}")
# st.write(f"**Dimensión:** {min_recovery_time['dimension']} m²")
# st.write(f"**Precio de compra:** {min_recovery_time['pricepop']} EUR")
# st.write(f"**Precio de renta mensual:** {min_recovery_time['price_rent']} EUR")
# st.write(f"**Tiempo para recuperar la inversión:** {min_recovery_time['time_to_recover']:2f} años")

# # Gráfico de barras para el tiempo de recuperación de la inversión
# fig1 = go.Figure(data=[go.Bar(x=properties_df['id'], y=properties_df['time_to_recover'])])
# fig1.update_layout(title='Tiempo de recuperación de la inversión por propiedad', xaxis_title='ID de propiedad', yaxis_title='Tiempo de recuperación (años )')
# st.plotly_chart(fig1, use_container_width=True)


# st.header("Propiedad con mayor ganancia en 10 años")
# st.write(f"**ID:** {max_profit_10_years['id']}")
# st.write(f"**Ubicación:** {max_profit_10_years['neighbourhoodMun']}")
# st.write(f"**Habitaciones:** {max_profit_10_years['rooms']}")
# st.write(f"**Dimensión:** {max_profit_10_years['dimension']} m²")
# st.write(f"**Precio de compra:** {max_profit_10_years['pricepop']} EUR")
# st.write(f"**Precio de renta mensual:** {max_profit_10_years['price_rent']} EUR")
# st.write(f"**Ganancia en 10 años:** {max_profit_10_years['profit_10_years']} EUR (esto significa que no hay ganancia, sino una pérdida)")

# # Mostrar la tabla completa
# st.header("Datos de todas las propiedades")
# st.dataframe(properties_df)


# # Gráfico de barras para las ganancias en 10 años
# fig2 = go.Figure(data=[go.Bar(x=properties_df['id'], y=properties_df['profit_10_years'])])
# fig2.update_layout(title='Ganancias en 10 años por propiedad', xaxis_title='ID de propiedad', yaxis_title='Ganancias en 10 años (EUR)')
# st.plotly_chart(fig2, use_container_width=True)
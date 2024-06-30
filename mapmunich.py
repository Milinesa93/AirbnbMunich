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


# Leer el archivo CSV
file_path = 'top10munichairbnb.csv'
top10munich_df = pd.read_csv(file_path)

# Crear el título y la descripción en Streamlit
st.title('Análisis de inversión en los 10 barrios más populares de Munich')
st.subheader("Un grupo de inversionistas, solicitan un estudio sobre la ciudad de Munich cercano a Theresienwiese, donde se celebra todos los años el OctokerFest. Creen que invertir en esta zona, les dará mayores ganancias a futuro que en otras zonas de Munich. El objetivo de adquirir la propiedad, es convertirlo en un Airbnb, quieren determinar según los resultados si será para compartir o departamento entero, según cual da mayores ganancias.")
st.write('En este análisis se pretende determinar cuál de los 10 barrios más populares de Munich es el mejor para invertir en un apartamento turístico. Para ello se han tenido en cuenta diferentes variables como el precio medio de alquiler por barrio y las puntuaciones más altas por location.')
st.write('A continuación se muestra un mapa con los 10 barrios más populares de Munich.')

# Crear mapa centrado en Theresienwiese
# Crear mapa centrado en Theresienwiese
m = folium.Map(location=[48.13583263039702, 11.545248777231926], zoom_start=12)

# Crear popup con HTML y CSS para Theresienwiese
popup_html = """
<div style="font-family: Arial; color: black; max-width: 300px;">
    <strong>Barrio Octokerfest:</strong> Theresienwiese
</div>
"""
popup = folium.Popup(popup_html, max_width=300)

# Añadir el marcador con el popup mejorado
folium.Marker([48.13583263039702, 11.545248777231926], popup=popup).add_to(m)


# Añadir un círculo de 2 kilómetros de radio alrededor de Theresienwiese
folium.Circle(
    location=[48.13583263039702, 11.545248777231926],
    radius=2000,  # Radio en metros
    color='darkviolet',
    fill=True,
    fill_color='violet',
    fill_opacity=0.2
).add_to(m)


icon_path = 'logoairbnb.png'

# Añadir marcadores con iconos personalizados y popups mejorados
for idx, row in top10munich_df.iterrows():
    icon = folium.CustomIcon(icon_path, icon_size=(45, 35))  # Ajusta el tamaño del icono según sea necesario
    
    # Crear popup con HTML y CSS para mejor visualización
    popup_html = f"""
    <div style="font-family: Arial; color: black; max-width: 300px;">
        <strong>Neighbourhood:</strong> {row['neighbourhood']}<br><br>
        <strong>Room Type:</strong> {row['room_type']}<br><br>
        <strong>Price per day:</strong> ${row['price_perday']}<br><br>
        <strong>Review Scores Location:</strong> {row['review_scores_location']}
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
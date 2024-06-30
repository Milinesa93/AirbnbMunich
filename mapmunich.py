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



# Leer el archivo CSV
file_path = 'top10munichairbnb.csv'
top10munich_df = pd.read_csv(file_path)

file_pathprop = 'properties.csv'
properties_df = pd.read_csv(file_pathprop)


base="dark"
primaryColor="#ffffff"
backgroundColor="#0b5d75"
secondaryBackgroundColor="#927600"



# Crear el título y la descripción en Streamlit
st.title('Análisis de inversión en Munich, cercanías de Theresienwiese')
st.subheader("Un grupo de inversionistas solicita un estudio sobre la ciudad de Munich cerca de Theresienwiese, donde se celebra el Oktoberfest todos los años. Creen que invertir en esta zona les dará mayores ganancias a futuro que en otras zonas de Munich. El objetivo de adquirir la propiedad es convertirla en un Airbnb y quieren determinar según los resultados si será para compartir o departamento entero, según cuál genere mayores ganancias.")
st.write('En este análisis se pretende determinar cuál de los 10 barrios más populares de Munich es el mejor para invertir en un apartamento turístico. Para ello se han tenido en cuenta diferentes variables como el precio medio de alquiler por barrio y las puntuaciones más altas por ubicación.')
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

# Datos de las propiedades
data = {
    'id': ['Maxvorstadt64m²', 'Maxvorstadt54m²', 'Ludwigsvorstadt Isar.26m²', 'Maxvorstadt24m²'],
    'neighbourhoodMun': ['Maxvorstadt', 'Maxvorstadt', 'Ludwigsvorstadt Isarvorstadt', 'Maxvorstadt'],
    'rooms': [4, 2, 1, 1],
    'dimension': [64, 54, 26, 24],
    'pricepop': [872900, 715000, 318000, 399000],
    'price_rent': [2000, 1800, 1200, 1200]
}

df = pd.DataFrame(data)

# Calcular el tiempo de recuperación de la inversión
df['time_to_recover'] = df['pricepop'] / (df['price_rent'] * 12)

# Calcular las ganancias en 10 años
df['profit_10_years'] = (df['price_rent'] * 12 * 10) - df['pricepop']

# Identificar la propiedad con menor tiempo de recuperación y mayor ganancia en 10 años
min_recovery_time = df.loc[df['time_to_recover'].idxmin()]
max_profit_10_years = df.loc[df['profit_10_years'].idxmax()]

# Configurar la página de Streamlit
st.title("Análisis de Propiedades")

st.header("Propiedad con menor tiempo de recuperación de la inversión")
st.write(f"**ID:** {min_recovery_time['id']}")
st.write(f"**Ubicación:** {min_recovery_time['neighbourhoodMun']}")
st.write(f"**Habitaciones:** {min_recovery_time['rooms']}")
st.write(f"**Dimensión:** {min_recovery_time['dimension']} m²")
st.write(f"**Precio de compra:** {min_recovery_time['pricepop']} EUR")
st.write(f"**Precio de renta mensual:** {min_recovery_time['price_rent']} EUR")
st.write(f"**Tiempo para recuperar la inversión:** {min_recovery_time['time_to_recover']:.2f} años")

st.header("Propiedad con mayor ganancia en 10 años")
st.write(f"**ID:** {max_profit_10_years['id']}")
st.write(f"**Ubicación:** {max_profit_10_years['neighbourhoodMun']}")
st.write(f"**Habitaciones:** {max_profit_10_years['rooms']}")
st.write(f"**Dimensión:** {max_profit_10_years['dimension']} m²")
st.write(f"**Precio de compra:** {max_profit_10_years['pricepop']} EUR")
st.write(f"**Precio de renta mensual:** {max_profit_10_years['price_rent']} EUR")
st.write(f"**Ganancia en 10 años:** {max_profit_10_years['profit_10_years']} EUR (esto significa que no hay ganancia, sino una pérdida)")

# Mostrar la tabla completa
st.header("Datos de todas las propiedades")
st.dataframe(df)
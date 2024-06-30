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
import streamlit.components.v1 as components
import folium

file_path = 'analisis top 10/top10munichairbnb.csv'
top10munich_df = pd.read_csv('analisis top 10/top10munichairbnb.csv')

#crear mapa con las coordenadas de los 10 barrios
st.title('Análisis de inversión en los 10 barrios más populares de Munich')
st.subheader ("Un grupo de inversionistas, solicitan un estudio sobre la ciudad de Munich cercano a Theresienwiese, donde se celebra todos los años el OctokerFest. Creen que invertir en esta zona, les dara mayores ganancias a futuro que en otras zonas de Munich. El objetivo de adquirir la propiedad, es convertirlo en un Airbnb, quieren determinar según los resultados si será para compartir o departamento entero, según cual da mayores ganancias. ")
st.write('En este análisis se pretende determinar cuál de los 10 barrios más populares de Munich es el mejor para invertir en un apartamento turístico. Para ello se han tenido en cuenta diferentes variables como el precio medio de alquiler por barrio y las puntuaciones más altas por location ')
st.write('A continuación se muestra un mapa con los 10 barrios más populares de Munich')    

#Crear mapa centrado en un punto inicial en Theresienwiese : 
48.13651999254395, 11.54404714766402
m = folium.Map(location=[48.13651999254395, 11.54404714766402], zoom_start=12)

# Añadir puntos en el mapa
for index, row in top10munich_df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['neighborhood']).add_to(m)

# Mostrar el mapa
components.html(m._repr_html_(), width=800, height=600)
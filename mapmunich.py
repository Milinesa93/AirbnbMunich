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
from geopy.geocoders import Nominatim
import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
import pandas as pd
from geopy.geocoders import GoogleV3
import requests
import streamlit as st
from streamlit_folium import folium_static

file_path = 'top10munichairbnb.csv'
top10munich_df = pd.read_csv('top10munichairbnb.csv')

#crear mapa con las coordenadas de los 10 barrios
st.title('Análisis de inversión en los 10 barrios más populares de Munich')
st.subheader ("Un grupo de inversionistas, solicitan un estudio sobre la ciudad de Munich cercano a Theresienwiese, donde se celebra todos los años el OctokerFest. Creen que invertir en esta zona, les dara mayores ganancias a futuro que en otras zonas de Munich. El objetivo de adquirir la propiedad, es convertirlo en un Airbnb, quieren determinar según los resultados si será para compartir o departamento entero, según cual da mayores ganancias. ")
st.write('En este análisis se pretende determinar cuál de los 10 barrios más populares de Munich es el mejor para invertir en un apartamento turístico. Para ello se han tenido en cuenta diferentes variables como el precio medio de alquiler por barrio y las puntuaciones más altas por location ')
st.write('A continuación se muestra un mapa con los 10 barrios más populares de Munich')    


# Crear mapa centrado en Theresienwiese
m = folium.Map(location=[48.13583263039702, 11.545248777231926], zoom_start=12)

folium.Marker([48.13583263039702, 11.545248777231926], popup='Theresienwiese').add_to(m)

# Añadir los puntos al mapa
for idx, row in top10munich_df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['neighbourhood'],
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)



folium_static(m)
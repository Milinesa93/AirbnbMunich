import re
from colorama import Fore
import requests

inmobiliaria = "https://www.portamondial.com/es/inmobiliaria/buscar/?kaufart=comprar&land=de&region=bav&unterregion=&ort=muenchen-ludwigsvorstadt-isarvorstadt,muenchen-maxvorstadt&objektart=&preis=&schlafzimmer=0&badezimmer=0&wohnflaeche=0&grundstueck=0&ausstattung="
resultado = requests.get(inmobiliaria)
content = resultado.text
print(content)
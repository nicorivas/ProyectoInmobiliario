from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re

url = "https://www.toctoc.com/search/index2/?dormitorios=0&banos=0&superficieDesde=0&superficieHasta=0&precioDesde=0&precioHasta=0&moneda=UF&tipoArriendo=false&tipoVentaUsado=true&tipoVentaNuevo=true&tipoUltimasVentas=false&casaDepto=undefined&ordenarPorMoneda=UFCLP&ordenarDesc=false&ordernarPorFechaPublicacion=false&ordernarPorSuperficie=false&ordernarPorPrecio=false&pagina=1&textoBusqueda=providencia&tipoVista=lista&viewport=-34.2878148%2C-71.70881020000002%2C-32.919451%2C-69.76899430000003&comuna=Providencia&region=Regi%C3%B3n%20Metropolitana&atributos=&idle=false&zoom=14&buscando=true&vuelveBuscar=false&dibujaPoligono=true&resetMapa=true&animacion=true&idZonaHomogenea=0&esPrimeraBusqueda=false"


browser = webdriver.Chrome() #remover .exe para mac
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, "html5lib")

lista = {}
links = soup.find('ul', {'class':'list-calugas'})
for link in links:
    lista[link.h3.text]=link.a.get('href')

print(lista)


browser.close()
browser.quit()

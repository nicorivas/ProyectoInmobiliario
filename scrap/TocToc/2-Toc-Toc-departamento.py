from bs4 import BeautifulSoup
import bs4
from selenium import webdriver
import re

html = "https://www.toctoc.com/propiedades/compranuevo/departamento/providencia/bustos-departamentos-providencia/787089"
browser = webdriver.Chrome() #Sacar .exe para mac
browser.get(html)
html = browser.page_source

bsObj = BeautifulSoup(html, "html5lib")
nameList = bsObj.find('ul', {'class':'info_ficha'})

#Datos Edificio

edificio = {'nombre edificio': 'prueba'}
for name in nameList.findAll('li'):
    if len(name) == 2:
         edificio[name.contents[0].text] = name.contents[1].text
    if len(name) == 1:
        edificio[name.contents[0].text.split(':')[0]] = name.contents[0].text.split(':')[1]
    else:
        pass

print(edificio)




#lista = {}
#links = soup.find('ul', {'class':'list-calugas'})
#for link in links:
#    lista[link.h3.text]=link.a.get('href')

#print(lista)



browser.close()
browser.quit()

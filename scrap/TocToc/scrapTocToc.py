from bs4 import BeautifulSoup
from selenium import webdriver
import time
import bs4
import requests

'''Basic functions for scraping TocToc.cl
Some of the html tags of this site are hidden and bs4 is unable to scrap. 
Selenium webdriver helps with this issue
with help of Chromedriver (using Chrome's source page viewer), 
so Google Chrome and Chromedriver must be installed. Another solution is using PhantomJS (needs to be
installed), a headless browser "in the shadow".
 Another issue is comes with the appartment data that is hidden behind a deployable menu. Using xpath and sellenium
 'click' method to open that menu and extract the appartment info. '''


#takes some search parameters and returns a url with the search results
def search_parameters(url):
    #search = input('Busqueda= ')
    district = input('Comuna: ')
    basic_url = url.split('comuna')
    #search_url = "textoBusqueda=" + str(search)
    final_url = basic_url[0]+ 'comuna' + str(district) + basic_url[1]
    print(final_url)
    return final_url

#Gets all urls pages from a search. It takes one url, and returns a list of url with different page number
def get_urls(url):
    url_ = url.split('pagina=1')
    page = True
    pages = []
    pagnum = 1
    counter = 0
    browser = webdriver.PhantomJS()  # chromedriver must be in path or set in the env. var. or in .Chrome(path/to/chromedriver)
    while page:
        url_1 = url_[0]+'pagina='+ str(pagnum)+url_[1]
        pages.append(url_1)
        pagnum += 1
        browser.get(url_1)
        url_2 = url_[0]+'pagina='+ str(pagnum)+url_[1]
        browser.get(url)
        time.sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, "html5lib")
        if len(soup.find('ul', {'class':'list-calugas'})) ==0:
            page = False
            counter += 1
            if counter == 1000:
                page = False
        print(url_2)
        try:
            print(len(soup.find('ul', {'class':'list-calugas'})))
            counter += 1
            print(counter)
            if len(soup.find('ul', {'class':'list-calugas'})) == 0:
                page = False
        except:
            counter += 1
            print(counter)
            if counter ==10:
                page = False
    browser.close()
    browser.quit()
    print(pages)
    return pages


#Basic search for buildings, given a parameter it search for building within TocToc's database and returns a list
#with ["name of the building", url, house or apartment].

#Basic search for buildings, given a parameter it search for building within TocToc's database and returns a dictionary
#with "name of the building": url.

def base_building_search(url):
    browser = webdriver.PhantomJS()#chromedriver must be in path or set in the env. var. or in .Chrome(path/to/chromedriver)
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    soup = BeautifulSoup(html, "html5lib")
    lista = []
    links = soup.find('ul', {'class':'list-calugas'})#Tag with list of the names a urls of the buildings
    #print(links)
    for link in links:
        lista.append([link.h3.text,[link.get('data-latitude'),
                      link.get('data-longitude')], link.a.get('href'),
                     link.find('li', {'class': 'familia'}).find('span').text.split(' ')[0]]) #gets building's name, url and type
    browser.close()
    browser.quit()
    return lista



#Takes a building's name and its url and returns a dictionary with basic building data
def building_data(url, building_name):
    browser = webdriver.PhantomJS()  # Sacar .exe para mac
    browser.implicitly_wait(10)
    browser.get(url)
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    head_info = bsObj.find('div', {'class':"wrap-hfijo"})
    #head data
    edificio = {'nombre edificio': building_name}
    edificio['nombre'] = head_info.find('h1').text
    edificio['direccion'] = head_info.findAll('h2')[0].text.replace(' Ver ubicación', '')
    edificio['comuna-region'] = head_info.findAll('h2')[1].text.split(', ')[1]
    edificio[head_info.find('em').text] = head_info.find('strong').text
    edificio['codigo'] = head_info.find('li', {'class':'cod'}).text.split(': ')[1]
    nameList = bsObj.find('ul', {'class': 'info_ficha'})#Tags with building data
    # bulding data
    for name in nameList.findAll('li'):
        if len(name) == 2:
            edificio[name.contents[0].text] = name.contents[1].text
        if len(name) == 1:
            edificio[name.contents[0].text.split(':')[0]] = name.contents[0].text.split(':')[1]
        else:
            pass
    browser.close()
    browser.quit()
    return(edificio)


#Takes a building name and it url (from base_building_search) and returns a nested dictionary of
# the buildings's apartment. The info is hidden in a deployable button that needs to be "open" before loading
# the page's source code.
def apartment_data(url, building_name):
    browser = webdriver.PhantomJS()
    browser.implicitly_wait(10)
    browser.get(url)
    browser.find_elements_by_xpath('//*[@id="btnVerPlantasCabecera"]')[0].click() #looks for button with info and clicks it
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    head_info = bsObj.find('div', {'class':"wrap-hfijo"})
    main_search = bsObj.findAll('div', {'class':'info-modelo'}) #where is data
    build_aps = {building_name:{}}
    build_aps['codigo'] = head_info.find('li', {'class':'cod'}).text.split(': ')[1]
    n = 1
    for i in main_search: #creates the nested dict.
        aux = {}
        for j in i.findAll('li'):
            if len(j.contents) == 3:
                aux[j.contents[0].text] = j.contents[2].text
            else:
                aux[j.contents[0].text] = j.contents[1]
        build_aps[building_name][str(n)] = aux
        n += 1
    browser.close()
    browser.quit()
    return build_aps


def house_data(url, house_name):
    browser = webdriver.PhantomJS()  # Sacar .exe para mac
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    nameList = bsObj.find('ul', {'class': 'info_ficha'})  # Tags with building data
    # house data
    head_info = bsObj.find('div', {'class': "wrap-hfijo"})
    casa = {}
    casa['nombre casa'] = house_name
    casa['tipo de vivienda'] = 'casa'
    casa['nombre'] = head_info.find('h1').text
    casa['direccion'] = head_info.findAll('h2')[0].text.replace(' Ver ubicación', '').strip()
    try:
        casa['comuna-region'] = head_info.findAll('h2')[1].text.split(',')[-1]
    except:
        casa['comuna-region'] = head_info.findAll('h2')[0].text.replace(' Ver ubicación', '').strip().split(' ')[-3]
    try:
        casa[head_info.find('em').text] = head_info.find('div', {'class':'precio-b'}).find('strong').text
    except:
        casa[head_info.find('em').text] = head_info.find('div', {'class': 'precio-ficha'}).find('strong').text
    casa['codigo'] = head_info.find('li', {'class': 'cod'}).text.split(': ')[1]
    for name in nameList.findAll('li'):
        if len(name) ==1:
            casa[name.contents[0].text.split(':')[0]] = name.contents[0].text.split(':')[1]
        elif len(name) == 2:
            if type(name.contents[0]) is not bs4.element.NavigableString:
                casa[name.contents[0].text] = name.contents[1].text
            else:
                casa[name.contents[0]] = name.contents[1].text
        elif len(name) == 5:
            casa[name.contents[0].strip()] = name.contents[1].text
        else:
            try:
                casa[name.contents[1].text] = name.contents[3].text
            except:
                casa[name.contents[1].text] = name.contents[2].text
    browser.close()
    browser.quit()
    return casa

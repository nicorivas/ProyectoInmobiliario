from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

'''Basic functions for scraping TocToc.cl
Some of the html tags of this site are hidden and bs4 is unable to scrap. 
Selenium webdriver helps with this issue
with help of Chromedriver (using Chrome's source page viewer), 
so Google Chrome and Chromedriver must be installed. Another solution is using PhantomJS (needs to be
installed), a headless browser "in the shadow" '''


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
        url_2 = url_[0]+'pagina='+ str(pagnum)+url_[1]
        browser.get(url)
        time.sleep(5)
        html = browser.page_source
        #html= requests.get(url_2)
        soup = BeautifulSoup(html, "html5lib")
        print(url_2)
        try:
            print(len(soup.find('ul', {'class':'list-calugas'})))
            counter +=1
            print(counter)
            if len(soup.find('ul', {'class':'list-calugas'}))==0:
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

#Basic search for buildings, given a parameter it search for building within TocToc's database and returns a dictionary
#with "name of the building": url.
def base_building_search(url):
    browser = webdriver.PhantomJS()#chromedriver must be in path or set in the env. var. or in .Chrome(path/to/chromedriver)
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, "html5lib")

    lista = {}
    links = soup.find('ul', {'class':'list-calugas'})#Tag with list of the names a urls of the buildings
    for link in links:
        lista[link.h3.text]=link.a.get('href')#gets building's name and url

    browser.close()
    browser.quit()
    return lista



#Takes a building's name and its url and returns s dictionary with basic building data
def building_data(url, building_name):
    browser = webdriver.PhantomJS()  # Sacar .exe para mac
    browser.get(url)
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    nameList = bsObj.find('ul', {'class': 'info_ficha'})#Tags with building data

    # Datos Edificio
    edificio = {'nombre edificio': building_name}
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




from bs4 import BeautifulSoup
from selenium import webdriver
import time


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
        browser.get(url_1)
        time.sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, "html5lib")
        if len(soup.find('ul', {'class':'list-calugas'})) ==0:
            page=False
            counter += 1
            if counter ==100:
                page= False
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



#Takes a building's name and its url and returns a dictionary with basic building data
def building_data(url, building_name):
    browser = webdriver.PhantomJS()  # Sacar .exe para mac
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

def appartment_data(url, building_name):
    browser = webdriver.PhantomJS()  # Sacar .exe para mac
    browser.get(url)
    browser.find_elements_by_xpath('//*[@id="btnVerPlantasCabecera"]')[0].click()
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    main_search = bsObj.findAll('div', {'class':'info-modelo'})
    print(len(main_search))
    for i in main_search:
        print('break')
        #print(i.contents[1].text)
        print(i.findAll('li'))
    browser.close()
    browser.quit()
    return


from bs4 import BeautifulSoup  #For scraping HTML
from selenium import webdriver  #To navigate and get web page source code
import time  # For making pause and let the webdriver load the source code
import bs4 #To get the bsf type object
from selenium.webdriver.common.keys import Keys #To use Tab key
from selenium.webdriver.chrome.options import Options #To use chrome options, as headless
import logging #To suppress Console dialogs of webdriver.
from selenium.webdriver.remote.remote_connection import LOGGER #To suppress Console dialogs of webdriver.
import re #To search for keywords in urls (new building)


'''Basic functions for scraping TocToc.cl
Some of the html tags of this site are hidden and bs4 and requests is unable to scrap. 
Selenium webdriver helps with this with help from Chromedriver (using Chrome's source page viewer), 
so Google Chrome and Chromedriver must be installed. 
Another issue is comes with the appartment data that is hidden behind a deployable menu. Xpath and selenium
 'click' method opens that menu and extract the apartment info. '''



def search_parameters(url):

    '''Takes some search parameters and returns a url with the search results'''

    district = input('Comuna: ')
    basic_url = url.split('comuna')
    final_url = basic_url[0]+ 'comuna' + str(district) + basic_url[1]
    print(final_url)
    return final_url


def get_urls(url):

    '''Gets all urls pages from a search. It takes one url, and returns
    a list of url with different page number'''
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    #browser = webdriver.PhantomJS()  # PhantomJS must be in path or  .PhantomJS(path/to/chromedriver)
    browser.get(url)
    url_ = url.split('pagina=1')
    page = True
    pages = []
    pagnum = 1
    counter = 0

    while page:
        url_1 = url_[0] + 'pagina=' + str(pagnum) + url_[1]
        browser.get(url_1)
        time.sleep(5) #Give time to load the page
        html = browser.page_source
        soup = BeautifulSoup(html, "html5lib")
        try:
            if len(soup.find('ul', {'class':'list-calugas'})) == 0:
                page = False
            else:
                pages.append(url_1)
                pagnum += 1
        except:
            counter += 1
            if counter == 1000:
                page = False
    browser.close()
    browser.quit()
    return pages




def base_building_search(url):

    '''Basic search for buildings, given a parameter it search for building within TocToc's database
    and returns a list with ["name of the building", [Lat, Long], url, house or apartment].'''

    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    browser.get(url)
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html, "html5lib")
    list = []
    links = soup.find('ul', {'class':'list-calugas'})#Tag with list of the names and urls of the buildings
    for link in links:
        regexp = re.compile(r'compranuevo')
        if regexp.search(link.a.get('href')):
            list.append([link.h3.text, [link.get('data-latitude'),
                         link.get('data-longitude')], 'Nuevo' ,link.a.get('href'),
                         link.find('li', {'class': 'familia'}).find('span').text.split(' ')[0]]) #gets building's name, url and type
        else:
            list.append([link.h3.text, [link.get('data-latitude'),
                                        link.get('data-longitude')], 'Usado', link.a.get('href'),
                         link.find('li', {'class': 'familia'}).find('span').text.split(' ')[
                             0]])  # gets building's name, url and type
    browser.close()
    browser.quit()
    return list



#
def building_data(url, building_name):

    '''Takes a building's name and its url and returns a dictionary with basic building data'''

    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac)  # Sacar .exe para mac
    browser.implicitly_wait(10)
    browser.get(url)
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    head_info = bsObj.find('div', {'class':"wrap-hfijo"})
    #head data of building
    building = {'nombre edificio': building_name}
    building['nombre'] = head_info.find('h1').text
    building['direccion'] = head_info.findAll('h2')[0].text.replace(' Ver ubicación', '').strip()
    building['comuna-region'] = head_info.findAll('h2')[1].text.split(', ')[1]
    building[head_info.find('em').text] = head_info.find('strong').text
    building['codigo'] = head_info.find('li', {'class':'cod'}).text.split(': ')[1]
    nameList = bsObj.find('ul', {'class': 'info_ficha'}) #Tags with building data
    # bulding data
    for name in nameList.findAll('li'):
        if len(name) == 2:
            building[name.contents[0].text] = name.contents[1].text
        elif len(name) == 1:
            building[name.contents[0].text.split(':')[0]] = name.contents[0].text.split(':')[1]
        else:
            pass
    browser.close()
    browser.quit()
    return building



def apartment_data(url, building_name):

    '''Takes a building name and it url (from base_building_search) and returns a nested dictionary of
    the buildings's apartment. The info is hidden in a deployable button that needs to be "open" before loading
    the page's source code.'''

    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # fatal
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    #browser = webdriver.PhantomJS()
    time.sleep(10)  #wait for page to be loaded.
    browser.get(url)
    try:
        browser.find_elements_by_xpath('//*[@id="btnVerPlantasCabecera"]')[0].click()  #looks for button with info and clicks it
        html = browser.page_source
        bsObj = BeautifulSoup(html, "html5lib")
        head_info = bsObj.find('div', {'class': "wrap-hfijo"})
        main_search = bsObj.findAll('div', {'class': 'info-modelo'})  # where is data
        build_aps = {}
        build_aps['nombre_edificio'] = building_name
        build_aps['codigo'] = head_info.find('li', {'class': 'cod'}).text.split(': ')[1]
        build_aps['precio_publicacion'] = head_info.find('div', {'class': 'precio-b'}).strong.text
        build_aps['precio_publicacion'] = head_info.find('em', {'class': 'precioAlternativo'}).strong.text

        n = 1
        for i in main_search:  # creates the nested dict.
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

    except:
        html = browser.page_source
        bsObj = BeautifulSoup(html, "html5lib")
        head_info = bsObj.find('div', {'class':"wrap-hfijo"})
        main_search = bsObj.find('ul', {'class':'info_ficha'}) #where is data
        build_aps = {}
        build_aps['nombre_edificio'] = building_name
        build_aps['codigo'] = head_info.find('li', {'class':'cod'}).text.split(': ')[1]
        build_aps['precio_publicacion'] = head_info.find('div', {'class':'precio-b'}).strong.text
        build_aps['precio_alternativo'] = head_info.find('em', {'class':'precioAlternativo'}).strong.text
        for i in main_search:  #creates the nested dict.
            try:
                build_aps[i.find('span').text] = i.find('strong').text
                #build_aps[i.contents[0]].text = i.contents[1].text

            except:
                try:
                    build_aps[i.contents[0].strip()] = i.contents[1].text
                except:
                    continue
        browser.close()
        browser.quit()
        return build_aps


def house_data(url, house_name):

    ''' Takes a house url and a house name and returns a dictionary with the house's data.
    The page doesn't give the house's data in the same way for all the cases, so the functions needs a lot
    of 'if' and 'try' statements. Is not elegant, but it works fine. '''

    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # fatal
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    browser.get(url)
    time.sleep(10)
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    nameList = bsObj.find('ul', {'class': 'info_ficha'})  # Tags with building data
    # head house data
    head_info = bsObj.find('div', {'class': "wrap-hfijo"})
    house = {}
    house['nombre casa'] = house_name
    house['tipo de vivienda'] = 'casa'
    house['nombre'] = head_info.find('h1').text
    house['direccion'] = head_info.findAll('h2')[0].text.replace(' Ver ubicación', '').strip()
    try:
        house['comuna-region'] = head_info.findAll('h2')[1].text.split(',')[-1]
    except:
        house['comuna-region'] = head_info.findAll('h2')[0].text.replace(' Ver ubicación', '').strip().split(' ')[-3]
    try:
        house[head_info.find('em').text] = head_info.find('div', {'class':'precio-b'}).find('strong').text
    except:
        house[head_info.find('em').text] = head_info.find('div', {'class': 'precio-ficha'}).find('strong').text
    house['codigo'] = head_info.find('li', {'class': 'cod'}).text.split(': ')[1]
    for name in nameList.findAll('li'):
        if len(name) ==1:
            house[name.contents[0].text.split(':')[0]] = name.contents[0].text.split(':')[1]
        elif len(name) == 2:
            if type(name.contents[0]) is not bs4.element.NavigableString:
                house[name.contents[0].text] = name.contents[1].text
            else:
                house[name.contents[0]] = name.contents[1].text
        elif len(name) == 5:
            house[name.contents[0].strip()] = name.contents[1].text
        else:
            try:
                house[name.contents[1].text] = name.contents[3].text
            except:
                house[name.contents[1].text] = name.contents[2].text
    browser.close()
    browser.quit()
    return house


def apartment_value_data(url, user, password):

    ''' takes a url of a apartment, an email/user and password and returns a dictionary with TocToc's appraisal'''

    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # fatal error in console
    LOGGER.setLevel(logging.WARNING) #Suppress console wartnings
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    #browser = webdriver.PhantomJS()
    appraisal_data = {}
    browser.get(url)
    time.sleep(10)
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    bsObj2 = bsObj.find('ul', {'class': 'listado-plantas'}).findAll('li')
    n = 1
    browser.find_elements_by_xpath('//*[@id="listado-plantas"]/li['+ str(n) +']/div[3]/a')[0].click() #open logging
    alert = browser.find_elements_by_xpath('//*[@id="IngresoUsuario_CorreoElectronico"]')[0] # Finds logging form
    time.sleep(5)
    alert.send_keys(user + Keys.TAB + password) # Fills logging form
    browser.find_elements_by_xpath('//*[@id="btnIngresoUsuarioPop"]')[0].click() #logging
    time.sleep(5)
    for i in bsObj2: #loop to find all building's appraisals
        if i.find('a') is not None:
            try:
                if n > 10: #max number of appraisals for building
                    return appraisal_data
                    browser.close()
                    browser.quit()
                else:
                    time.sleep(7)
                    browser.find_elements_by_xpath('//*[@id="listado-plantas"]/li[' + str(n) + ']/div[3]/a')[0].click()
                    time.sleep(5)
                    html = browser.page_source
                    bsObj3 = BeautifulSoup(html, "html5lib")
                    head_info = bsObj3.find('div', {'class': "wrap-hfijo"})
                    apt = {}
                    apt['codigo'] = head_info.find('li', {'class': 'cod'}).text.split(': ')[1]
                    apt['depto'] = bsObj3.findAll('td', {'class': 'cifra'})[0].text
                    apt['precio_referencia'] = bsObj3.find('div', {'class': 'cotiz-precio-ref'}).strong.text
                    apt['piso'] = bsObj3.findAll('td', {'class': 'cifra'})[1].text
                    apt['dormitorios'] = bsObj3.findAll('td', {'class': 'cifra'})[2].text
                    apt['banos'] = bsObj3.findAll('td', {'class': 'cifra'})[3].text
                    apt['orientacion'] = bsObj3.findAll('td', {'class': 'plantaOrientacion centrado'})[0].text
                    apt['m2_utiles'] = bsObj3.findAll('td', {'class': 'cifra'})[4].text
                    apt['m2_terraza'] = bsObj3.findAll('td', {'class': 'cifra'})[5].text
                    apt['m2_totales'] = bsObj3.findAll('td', {'class': 'cifra'})[6].text
                    appraisal_data[str(n)] = apt
                    n += 1
                    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform() #Close current appraisal window
                    browser.execute_script("window.stop();")
                    browser.back()
                    print(n)
            except:
                print('error 2')
                browser.close()
                browser.quit()
                return appraisal_data

    browser.close()
    browser.quit()
    return appraisal_data


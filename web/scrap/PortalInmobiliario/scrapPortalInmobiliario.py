from bs4 import BeautifulSoup  #For scraping HTML
from selenium import webdriver  #To navigate and get web page source code
import time  # For making pause and let the webdriver load the source code
import bs4 #To get the bsf type object
from selenium.webdriver.common.keys import Keys #To use Tab key
from selenium.webdriver.chrome.options import Options #To use chrome options, as headless
import logging #To suppress Console dialogs of webdriver.
from selenium.webdriver.remote.remote_connection import LOGGER #To suppress Console dialogs of webdriver.
import re #To search for keywords in urls (new building)

def search_parameters_PI(url):

    '''Takes some search parameters and returns a url with the search results'''

    district = input('Comuna: ')
    basic_url = url.split('comuna')
    final_url = basic_url[0]+ 'comuna' + str(district) + basic_url[1]
    print(final_url)
    return final_url



def get_urls_PI(url):

    '''Gets all urls pages from a search. It takes one url, and returns
    a list of url with different page number'''

    url_ = url.split('pg=1')
    page = True
    pages = []
    pagnum = 1
    counter = 0
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options = options)
    browser.get(url)
    while page:
        url_1 = url_[0] + 'pg=' + str(pagnum) + url_[1]
        browser.get(url_1)
        time.sleep(2) #Give time to load the page
        html = browser.page_source
        bsObj = BeautifulSoup(html, "html5lib")
        try:
            end = bsObj.find('span', {'class': 'textual-pager text-muted'}).text.split(' ')[-1]
            begin = bsObj.find('span', {'class': 'textual-pager text-muted'}).text.split(' ')[3]
        except:
            return pages
        try:
            if len(bsObj.find('div', {'class':'products-list'})) == 1 or begin == end:
                page = False
                pages.append(url_1)
            else:
                pages.append(url_1)
                pagnum += 1
        except:
            counter += 1
            if counter == 800:
                page = False
        print(pagnum)
    browser.close()
    browser.quit()
    return pages

def clean_appraisals_PI(user, password):

    '''Errases the appraisal list in PortalInmobiliario, so maximum is never reach'''

    url = 'https://www.portalinmobiliario.com'
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # only fatal error in console
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    try:
        browser.get(url)
        browser.find_elements_by_xpath('//*[@id="show-login-prompt"]')[0].click()  # open logging
        time.sleep(2)
        alert = browser.find_elements_by_xpath('//*[@id="txtEmail"]')[0]  # Finds logging form
        time.sleep(1)
        alert.send_keys(user + Keys.TAB + password)  # Fills logging form
        browser.find_elements_by_xpath('//*[@id="linkIngresar"]')[0].click()  # logging
        time.sleep(2)
        url = 'https://www.portalinmobiliario.com/miportal/miscotizaciones'
        browser.get(url)
        html = browser.page_source
        bsObj = BeautifulSoup(html, "html5lib")
        for i in bsObj.find('table', {'class': 'table cz-list'}).findAll('input', {'type':'checkbox'}):
            browser.find_elements_by_xpath('//*[@id="' + i.get('id') + '"]')[0].click()
        browser.find_elements_by_xpath('//*[@id="btnEliminaCotizaciones"]')[0].click()
        browser.close()
        browser.quit()
    except:
        return
    return


def base_building_search_PI(url):

    '''Basic search for buildings, given a parameter it search for building within Portal Inmboliario's database
    and returns a list with ["name of the building", [Lat, Long], url, house or apartment].'''
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options= options)
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    soup = BeautifulSoup(html, "html5lib")
    list = []
    links = soup.find('div', {'class':'products-list'})#Tag with list of the names and urls of the buildings
    regexp = re.compile(r'Handler')
    regexp2 = re.compile(r'departamento')
    base_url = 'https://www.portalinmobiliario.com'
    for link in links:
        #print(link)
        try:
            if not regexp.search(link.a.get('href')):
                if regexp2.search(link.a.get('href')):
                    list.append(['departamento', base_url + link.a.get('href'),
                                 link.find('span', {'class': 'product-type-title'}).text.replace(',', '')])
                else:
                    list.append(['casa', base_url + link.a.get('href'),
                                 link.find('span', {'class': 'product-type-title'}).text.replace(',', '')])
        except:
            continue
    browser.close()
    browser.quit()
    return list

def building_data_PI(url):

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
    browser.get(url)
    time.sleep(3)
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    head_info = bsObj.find('div', {'class':"col-sm-10 col-md-8"})
    #head data of building
    building = {'name': head_info.find('h1', {'role':'heading'}).text}
    building['addressStreet'] = bsObj.find('section',
                                       {'class':'project-location-section'}).find('p', {'class':'prj-map-addr-obj'}).text
    building['coordinates'] = [bsObj.find('meta', {'property': 'og:latitude'}).attrs['content'],
                               bsObj.find('meta', {'property': 'og:longitude'}).attrs['content']]
    building['lat'] =bsObj.find('meta', {'property': 'og:latitude'}).attrs['content']
    building['lat'] =bsObj.find('meta', {'property': 'og:longitude'}).attrs['content']
    building['url'] = url
    comunareg = head_info.find('div', {'class':'bcrumbs prj-bcrumbs'}).findAll('span', {'itemprop':'title'})
    building['addressCommune'] = comunareg[-1].text
    building['addressRegion'] = comunareg[-2].text
    building['marketPrice'] = head_info.find('span', {'class':'prj-price-range-lower'}).text
    building['code'] = head_info.find('span', {'class':'prj-code'}).text.split(' ')[1]
    nameList = bsObj.findAll('div', {'class': 'project-feature-item'}) #Tags with building data
    # building data
    building['propertyType'] = nameList[0].text.strip()
    building['bedrooms'] = nameList[1].text.strip()
    building['bathrooms'] = nameList[2].text.strip()
    browser.close()
    browser.quit()
    return building


def apartment_data_PI(url):

    '''Takes an apartment's url (from base_building_search) and returns a nested dictionary of
    the apartments data. Only apartment that are for sale'''

    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # fatal errors
    LOGGER.setLevel(logging.WARNING) #supress console messages
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    time.sleep(5)  #wait for page to be loaded.
    browser.get(url)
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    head_info = bsObj.find('div', {'class': "media-block"})
    #main_search = bsObj.findAll('div', {'class': 'property-data-sheet clearfix'})  # where is data
    apt = {}
    apt['name'] = head_info.find('h4', {'class':'media-block-title'}).text.strip()
    apt['code'] = bsObj.find('p', {'class': 'operation-internal-code'}).text.split(': ')[1]
    apt['propertyType'] = 'departamento'
    apt['fecha_publicacion'] = bsObj.findAll('p', {'class': 'operation-internal-code'})[1].text.split(': ')[1]
    apt['coordinates'] = [bsObj.find('meta', {'property': 'og:latitude'}).attrs['content'],
                               bsObj.find('meta', {'property': 'og:longitude'}).attrs['content']]
    apt['lat'] = bsObj.find('meta', {'property': 'og:latitude'}).attrs['content']
    apt['lat'] = bsObj.find('meta', {'property': 'og:longitude'}).attrs['content']
    apt['url'] = url
    apt['marketPrice2'] = head_info.find('p', {'class': 'price'}).text
    apt['marketPrice'] = head_info.find('p', {'class': 'price-ref'}).text
    apt['addressStreet'] = bsObj.find('div', {'class':'data-sheet-column data-sheet-column-address'}).p.text.strip()
    for i in bsObj.find('div', {'class':'data-sheet-column data-sheet-column-programm'}).p.stripped_strings:
        apt[str(i).split('\xa0')[1]] = str(i).split('\xa0')[0]
    for i in bsObj.find('div', {'class':'data-sheet-column data-sheet-column-area'}).p.stripped_strings:
        apt[str(i).split('\xa0')[1]] = str(i).split('\xa0')[0]

    browser.close()
    browser.quit()
    return apt

def house_data_PI(url):

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
    options.add_argument("--log-level=3")  # only fatal error in console
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    bsObj = BeautifulSoup(html, "html5lib")
    # head house data
    head_info = bsObj.find('div', {'class': "media-block"})
    house = {}
    house['name'] = head_info.find('h4', {'class':'media-block-title'}).text.strip()
    house['code'] = bsObj.find('p', {'class': 'operation-internal-code'}).text.split(': ')[1]
    house['fecha-publicacion'] = bsObj.findAll('p', {'class': 'operation-internal-code'})[1].text.split(': ')[1]
    house['coordinates'] = [bsObj.find('meta', {'property': 'og:latitude'}).attrs['content'],
                               bsObj.find('meta', {'property': 'og:longitude'}).attrs['content']]
    house['lat'] = bsObj.find('meta', {'property': 'og:latitude'}).attrs['content']
    house['lat'] = bsObj.find('meta', {'property': 'og:longitude'}).attrs['content']
    house['url'] = url
    house['marketPrice2'] = head_info.find('p', {'class': 'price'}).text
    house['marketPrice'] = head_info.find('p', {'class': 'price-ref'}).text
    house['addressStreet'] = bsObj.find('div', {'class':'data-sheet-column data-sheet-column-address'}).p.text.strip()
    for i in bsObj.find('div', {'class':'data-sheet-column data-sheet-column-programm'}).p.stripped_strings:
        house[str(i).split('\xa0')[1]] = str(i).split('\xa0')[0]
    for i in bsObj.find('div', {'class':'data-sheet-column data-sheet-column-area'}).p.stripped_strings:
        house[str(i).split('\xa0')[1]] = str(i).split('\xa0')[0]

    browser.close()
    browser.quit()
    return house

def apartment_appraisal_data_PI(url ,user, password):

    '''Takes a building project an gets de apartment appraisal data'''

    options = Options()
    options.add_argument("--headless")  # Runs Chrome with headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # only fatal error in console
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    browser.get(url)
    htmlC = browser.page_source
    cords = BeautifulSoup(htmlC, "html5lib")
    coordinates = [cords.find('meta', {'property': 'og:latitude'}).attrs['content'],
                            cords.find('meta', {'property': 'og:longitude'}).attrs['content']]
    time.sleep(3)
    browser.find_elements_by_xpath('//*[@id="show-login-prompt"]')[0].click() #open logging
    time.sleep(5)
    alert = browser.find_elements_by_xpath('//*[@id="txtEmail"]')[0] # Finds logging form
    time.sleep(1)
    alert.send_keys(user + Keys.TAB + password) # Fills logging form
    browser.find_elements_by_xpath('//*[@id="linkIngresar"]')[0].click() #logging
    time.sleep(3)
    browser.find_elements_by_xpath('//*[@id="prj-show-cotizar"]')[0].click()  # open appraisal
    time.sleep(3)
    html = browser.page_source
    bsObj =  BeautifulSoup(html, "html5lib")
    n = 1
    list = []
    for elements in bsObj.find('ul', {'class':'slides clearfix'}):
        try:
            i = 1
            browser.find_elements_by_xpath('// *[ @ id = "prj-cotizacion-dialog"] / div / div / div / div[1] / div[1] / div[3] / div[1] / ul / li['+str(n)+'] / div[2]')[0].click()
            time.sleep(3)
            html2 = browser.page_source
            bsObj2 = BeautifulSoup(html2, "html5lib")
            for ap in bsObj2.find('select', {'class': 'form-control'}):
                apt  = {'number' : ap.text}
                apt['building_in'] = bsObj2.find('div', {'class': 'prj-name'}).text.split('Cód')[0].strip()
                apt['url'] = url
                apt['coordinates'] = coordinates
                apt['lat'] = coordinates[0]
                apt['lng'] = coordinates[1]
                try:
                    browser.find_elements_by_xpath('//*[@id="prj-cotizacion-dialog"]/div/div/div/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div/select/option['+str(i)+']')[0].click()
                except:
                    browser.find_elements_by_xpath('//*[@id="prj-cotizacion-dialog"]/div/div/div/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div/select/option')[0].click()
                browser.find_elements_by_xpath('//*[@id="prj-cotizacion-dialog"]/div/div/div/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/button')[0].click()
                time.sleep(3)
                html3 = browser.page_source
                bsObj3 = BeautifulSoup(html3, "html5lib")
                apt['code'] = bsObj3.find('span', {'class': 'prj-code'}).text.split(' ')[1]
                apt[bsObj3.findAll('th', {'class': 'c'})[0].text] = bsObj3.findAll('td', {'class': 'c'})[0].text
                apt[bsObj3.findAll('th', {'class': 'c'})[1].text] = bsObj3.findAll('td', {'class': 'c'})[1].text
                apt[bsObj3.findAll('th', {'class': 'c'})[2].text] = bsObj3.findAll('td', {'class': 'c'})[2].text
                apt[bsObj3.findAll('th', {'class': 'c'})[3].text] = bsObj3.findAll('td', {'class': 'c'})[3].text
                apt[bsObj3.findAll('th', {'class': 'r'})[0].text] = bsObj3.findAll('td', {'class': 'r'})[0].text
                apt[bsObj3.findAll('th', {'class': 'r'})[1].text] = bsObj3.findAll('td', {'class': 'r'})[1].text
                apt[bsObj3.findAll('th', {'class': 'r'})[2].text] = bsObj3.findAll('td', {'class': 'r'})[2].text
                apt[bsObj3.findAll('th', {'class': 'r'})[3].text] = bsObj3.findAll('td', {'class': 'r'})[3].text
                apt[bsObj3.findAll('th', {'class': 'r'})[4].text] = bsObj3.findAll('td', {'class': 'r'})[4].text
                apt['addressStreet'] = bsObj3.find('span', {'class': 'bcrumb-current'}).text
                apt['addressCommune'] = bsObj3.findAll('span', {'class': 'bcrumb-current'})[1].text.split(',')[1]
                browser.find_elements_by_xpath('//*[@id="prj-cotizacion-dialog"]/div/div/div/div[1]/div[1]/div[2]/div/div[4]/button')[0].click()
                list.append(apt)
                i += 1

                clean_appraisals_PI(user, password)

            n += 1
        except:
            continue
    browser.close()
    browser.quit()
    print(list)
    return list

def house_appraisal_data_PI(url ,user, password):

    '''Takes a building project an gets de apartment appraisal data'''

    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # only fatal error in console
    LOGGER.setLevel(logging.WARNING)
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    browser.get(url)
    htmlC = browser.page_source
    cords = BeautifulSoup(htmlC, "html5lib")
    coordinates = [cords.find('meta', {'property': 'og:latitude'}).attrs['content'],
                            cords.find('meta', {'property': 'og:longitude'}).attrs['content']]
    time.sleep(3)
    browser.find_elements_by_xpath('//*[@id="show-login-prompt"]')[0].click() #open logging
    time.sleep(3)
    alert = browser.find_elements_by_xpath('//*[@id="txtEmail"]')[0] # Finds logging form
    time.sleep(1)
    alert.send_keys(user + Keys.TAB + password) # Fills logging form
    browser.find_elements_by_xpath('//*[@id="linkIngresar"]')[0].click() #logging
    time.sleep(3)
    browser.find_elements_by_xpath('//*[@id="prj-show-cotizar"]')[0].click()  # open appraisal
    time.sleep(3)
    html = browser.page_source
    bsObj =  BeautifulSoup(html, "html5lib")
    n = 1
    list = []

    for elements in bsObj.find('ul', {'class':'slides clearfix'}):
        try:
            i = 1
            browser.find_elements_by_xpath('// *[ @ id = "prj-cotizacion-dialog"] / div / div / div / div[1] / div[1] / div[3] / div[1] / ul / li['+str(n)+'] / div[2]')[0].click()
            time.sleep(3)
            html2 = browser.page_source
            bsObj2 = BeautifulSoup(html2, "html5lib")
            for hous in bsObj2.find('select', {'class': 'form-control'}):
                house  = {'number' : hous.text}
                house['name'] = bsObj2.find('div', {'class': 'prj-name'}).text.split('Cód')[0].strip()
                house['url'] = url
                house['coordinates'] = coordinates
                house['lat'] = coordinates[0]
                house['lng'] = coordinates[1]
                try:
                    browser.find_elements_by_xpath('//*[@id="prj-cotizacion-dialog"]/div/div/div/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div/select/option['+str(i)+']')[0].click()
                except:
                    browser.find_elements_by_xpath('//*[@id="prj-cotizacion-dialog"]/div/div/div/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/div/div/select/option')[0].click()
                browser.find_elements_by_xpath('//*[@id="prj-cotizacion-dialog"]/div/div/div/div[1]/div[1]/div[3]/div[2]/div/div[2]/div/button')[0].click()
                time.sleep(3)
                html3 = browser.page_source
                bsObj3 = BeautifulSoup(html3, "html5lib")
                house['code'] = bsObj3.find('span', {'class': 'prj-code'}).text.split(' ')[1]
                house[bsObj3.findAll('th', {'class': 'c'})[0].text] = bsObj3.findAll('td', {'class': 'c'})[0].text
                house[bsObj3.findAll('th', {'class': 'c'})[1].text] = bsObj3.findAll('td', {'class': 'c'})[1].text
                house[bsObj3.findAll('th', {'class': 'r'})[0].text] = bsObj3.findAll('td', {'class': 'r'})[0].text
                house[bsObj3.findAll('th', {'class': 'r'})[1].text] = bsObj3.findAll('td', {'class': 'r'})[1].text
                house[bsObj3.findAll('th', {'class': 'r'})[2].text] = bsObj3.findAll('td', {'class': 'r'})[2].text
                house[bsObj3.findAll('th', {'class': 'r'})[3].text] = bsObj3.findAll('td', {'class': 'r'})[3].text
                house['addressStreet'] = bsObj3.find('span', {'class': 'bcrumb-current'}).text
                house['addressCommune'] = bsObj3.findAll('span', {'class': 'bcrumb-current'})[1].text.split(',')[1]
                browser.find_elements_by_xpath('//*[@id="prj-cotizacion-dialog"]/div/div/div/div[1]/div[1]/div[2]/div/div[4]/button')[0].click()
                print(house)
                list.append(house)
                i += 1
                clean_appraisals_PI(user, password)

            n += 1
        except:
            continue
    browser.close()
    browser.quit()
    return list



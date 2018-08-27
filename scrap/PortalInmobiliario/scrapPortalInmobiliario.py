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
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
    browser.get(url)
    #browser = webdriver.PhantomJS()  # PhantomJS must be in path or  .PhantomJS(path/to/chromedriver)
    while page:
        url_1 = url_[0] + 'pg=' + str(pagnum) + url_[1]
        browser.get(url_1)
        time.sleep(2) #Give time to load the page
        html = browser.page_source
        bsObj = BeautifulSoup(html, "html5lib")
        end = bsObj.find('span', {'class': 'textual-pager text-muted'}).text.split(' ')[-1]
        begin = bsObj.find('span', {'class': 'textual-pager text-muted'}).text.split(' ')[3]
        try:
            if len(bsObj.find('div', {'class':'products-list'})) == 1 or begin == end:
                page = False
                pages.append(url_1)
            else:
                pages.append(url_1)
                pagnum += 1
        except:
            counter += 1
            if counter == 1000:
                page = False
        print(pagnum)
    browser.close()
    browser.quit()
    return pages


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
    browser = webdriver.Chrome(chrome_options= options)  # Sacar .exe para mac
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


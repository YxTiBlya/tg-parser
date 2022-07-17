from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from transliterate import translit

import time
import config as cfg
import createRes as crExcel

options = webdriver.ChromeOptions()
options.add_experimental_option(
    'prefs', 
    {
        #'profile.managed_default_content_settings.javascript': 2,
        'profile.managed_default_content_settings.images': 2,
        'profile.managed_default_content_settings.mixed_script': 2,
        'profile.managed_default_content_settings.media_stream': 2,
        'profile.managed_default_content_settings.stylesheets':2
    }
)
options.add_argument("start-maximized")

def convert(msg):
    request, location = map(str, msg.split('/'))
    request, location = request.lower().strip(), location.lower().strip()
    location = translit(location, 'ru', reversed=True)
    location = location.replace('j', 'y')
    location = location.replace("'", '')
    return request, location

### 2GIS parsing
def p2gis(request_msg):
    request, location = convert(request_msg)
    url = cfg.twogis_url(request, location)

    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(cfg.wait_time)

    links = []
    req_result = []
    nextpage = 2

    try:
        try:
            driver.get(url)
            driver.find_element_by_xpath(cfg.xpath_close_footer).click()
            while True:
                time.sleep(1.5)

                articles = driver.find_elements_by_class_name("_1hf7139")
                for article in articles:
                    link = article.find_element_by_class_name("_1rehek").get_attribute('href')
                    links.append(link)

                cfg.btns_Pages = cfg.btns_Pages.replace(f'"{nextpage-1}"', f'"{nextpage}"')
                btn_Page = driver.find_element_by_xpath(cfg.btns_Pages)
                btn_Page.location_once_scrolled_into_view
                btn_Page.click()
                nextpage += 1
        except Exception as err:
            print(err)
        
        for link in links:
            driver.get(link)

            page = driver.page_source
            soup = BeautifulSoup(page, "lxml")

            name = soup.find("h1", class_="_d9xbeh").text

            try:
                main_adress = soup.find("span", class_="_er2xx9").find("a", class_="_2lcm958").text
            except Exception:
                main_adress = soup.find("span", class_="_er2xx9").text

            try:
                phone = soup.find("div", class_="_b0ke8").find("a").get("href")
                phone = phone[4:]
            except Exception:
                phone = "Нет"

            WApp = "Нет"
            try: 
                webs = soup.find_all("span", class_="_1dvs8n")
                for web in webs:
                    if web.text.strip() == "WhatsApp":
                        WApp = "Да"
                        break
            except Exception:
                pass

            req_result.append([name, main_adress, phone, WApp])

    except Exception as err:
        print(err)
    finally:
        print('Finally')
        driver.close()
        driver.quit()
        request_msg = request_msg.replace('/', '.')
        crExcel.create_Excel_Table2GIS(req_result, request_msg)
        return request_msg
###

### Avito parsing
def pAvito(request_msg):
    request, location = convert(request_msg)
    url = cfg.avito_url(request, location)

    req_result = []
    nextpage = 2

    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(cfg.wait_time)

    try:
        driver.get(url)
        while True:
            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')

            jobs = soup.find_all("div", class_="iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum")
            for vacancy in jobs:
                name = vacancy.find("h3", class_="title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO").text
                price = vacancy.find("span", class_="price-text-_YGDY text-text-LurtD text-size-s-BxGpL").text
                link = "https://www.avito.ru" + vacancy.find("a", class_="link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH").get("href")
                req_result.append([name, price, link])

            max_pagin = int(soup.find_all("span", class_="pagination-item-JJq_j")[-2].text)

            if nextpage <= max_pagin:
                url = url.replace(f"p={nextpage-1}", f"p={nextpage}")
                nextpage += 1
                driver.get(url)
            else:
                break

    except Exception as err:
        print(err)

    finally:
        print('Finally')
        driver.close()
        driver.quit()
        request_msg = request_msg.replace('/', '.')
        crExcel.create_Excel_TableAVITO(req_result, request_msg)
        return request_msg
###

### Youla parsing
def pYoula(request_msg):
    pass
###

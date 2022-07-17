TOKEN = '5363607292:AAFAkV9nttzNpQ6OcfkgtULrIHS-HKhUNwY' # token bot

def avito_url(req, loc):
    if req.find(' '):
        req = req.replace(' ', '+')
    if loc.find(' '):
        loc = loc.replace(' ', '_')

    url = f'https://www.avito.ru/{loc}?bt=1&localPriority=1&p=1&q={req}'

    return url

def twogis_url(req, loc):
    req = list(map(str, req.split()))

    if len(req) >= 2:
        req = f'{req[0]}%20{req[1]}' 
    else:
        req = f'{req[0]}'

    if loc == 'nizhniy novgorod':
        loc = "n_novgorod"
    if loc == 'moskva':
        loc = 'moscow'

    url = f'https://2gis.ru/{loc}/search/{req}/page/1'

    return url

wait_time = 5 # seconds

### For parsing 2GIS
input_search = "_1gvu1zk" # поле и кнопка поиска
result_req = "_1hf7139" # дивы выдачи
btns_Pages = '//span[@class="_19xy60y" and contains(text(), "1")]' # кнопки перехода на страницы
xpath_close_footer = '//div[@class="_euwdl0"]/*[name()="svg"]' # xpath для закрытие footer

name = "_d9xbeh" # название заведения
span_adress = "_er2xx9" # span адресса
main_adress = "_2lcm958" # адресс заведения
phone_number = "_b0ke8" # номер телефона заведения
show_number = "_1ns0i7c" # кнопка покааза телефона
webs = "_1dvs8n" # теги привязанных сетей
div_number = "_b0ke8" # div for a tag
###
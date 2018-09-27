import requests, string, csv, sys, time, os, re
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def extract_info():
    #Extrai as informacoes da pagina
    l1 = tree.xpath('//tr//td[1]/text()[normalize-space()]')
    l2 = tree.xpath('//tr//td//small[1]/text()[normalize-space()]')
    l3 = tree.xpath('//tr//td[@class="center"]/text()[normalize-space()]')
    l4 = tree.xpath('//*[@id="agks-cont-tb1"]//table//tbody//tr//td[4]/text()')
    l5 = tree.xpath('//*[@id="agks-cont-tb1"]//table//tbody//tr/td[5]/span/text()')
    #TIRA OS ESPACOS EM BRANCO e passa para o utf-8
    for i in range(0, len(l1)):
        l1[i] = l1[i].encode('utf-8').strip()
        l2[i] = l2[i].encode('utf-8').strip()
        l3[i] = l3[i].encode('utf-8').strip()
        l5[i] = l5[i].encode('utf-8').strip()
    lists(l1, l2, l3, l4, l5)

def lists(l1, l2, l3, l4, l5):
    j = 0
    #If l5 not D than dont add
    for i in range(0, len(l5)):
        city_state = []
        if l5[i] == 'D':
            #remove '(' and ')' and separate City and state into two different strings
            city_state = l2[i].split("(")
            city_state[1] = city_state[1].replace(")","")
            #insert only the informations with D(the Daily information)
            product.append(l1[i])
            city.append(city_state[0])
            state.append(city_state[1])
            price.append(l3[i])
            data.append(l4[i])
            freq.append(l5[i])

def csv_creator(product, city, state, price, data, freq):
    row = zip(product, city, data, state, price)
    #save the values into a list
    with open("tudocsvfile", "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in row:
            writer.writerow(val)
    

#evita que o chrome abra.
chrome_options = Options()
chrome_options.binary_location = GOOGLE_CHROME_BIN
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920x1080")
#Usa selenium que usa o chrome para navegar no site.
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
sit = ['/graos/milho','/graos/soja','/graos/cafe','/graos/feijao','/graos/trigo','/graos/arroz', 
'/carnes/aves', '/carnes/bovinos', '/carnes/bubalinos', '/carnes/caprinos', '/carnes/ovinos', '/carnes/suinos',
'/hortalicas/beterraba', '/hortalicas/cenoura', '/hortalicas/tomate',
'/frutas/banana', '/frutas/laranja', '/frutas/maca', '/frutas/uva', '/frutas/caqui', '/frutas/cacau', '/frutas/goiaba',
'/frutas/lima', '/frutas/mamao', '/frutas/manga', '/frutas/maracuja', '/frutas/melancia', '/frutas/melao', '/frutas/morango',
'/frutas/tangerina', '/diversos/acucar', '/diversos/algodao', '/diversos/alho', '/diversos/amendoin', '/diversos/azevem',
'/diversos/batata', '/diversos/cana-de-acucar', '/diversos/cebola', '/diversos/dende', '/diversos/erva-mate',
'/diversos/farelo-de-soja', '/diversos/farinha-de-mandioca', '/diversos/girassol', '/diversos/leite', '/diversos/mandioca','/diversos/ovos'
]
product = ['nomeproduto']
city = ['nomecidade']
state = ['UF']
price = ['preco']
data = ['datacorrente']
freq = []
for ct in range(0,len(sit)):
    driver.get("https://www.agrolink.com.br/cotacoes"+sit[ct]+"")
    print "https://www.agrolink.com.br/cotacoes"+sit[ct]+""
    page = requests.get(driver.current_url)
    tree = html.fromstring(page.content)
    extract_info()
    walk = 0
    aux = 2
    while (walk == 0):
        print aux
        p = str(aux)
        #Executa o javascript da paginacao e vai para a proxima pagina.
        driver.execute_script("javascript:navigateToPage('frmFiltroGeral-5231', " + p + ")")
        #verifica se ja passou da ultima pagina.
        last_page = tree.xpath('//*[@id="frmMercadoFisico-5181"]/div/span/text()')
        #para o loop
        if len(last_page) != 0:
        #if aux == 10:
            walk = 1
        else:
            time.sleep(5)
            #ATUALIZA O HTML
            page = driver.execute_script("return document.body.innerHTML")
            tree = html.fromstring(page)
            extract_info()
            aux = aux + 1
            
csv_creator(product, city, state, price, data, freq)
driver.close()
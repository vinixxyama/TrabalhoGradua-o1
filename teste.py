import requests, string, csv, sys, time, os
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def extrai_info():
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
    listas(l1, l2, l3, l4, l5)

def listas(l1, l2, l3, l4, l5):
    j = 0
    teste = 'D'
    #se for diferente de Dia nao adiciona
    for i in range(0, len(l5)):
        if l5[i] == teste:
            produto.append(l1[i])
            ce.append(l2[i])
            preco.append(l3[i])
            data.append(l4[i])
            freq.append(l5[i])

#evita que o chrome abra.
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
#Usa selenium que usa o chrome para navegar no site.
driver = webdriver.Chrome(chrome_options=chrome_options)
sit = '/graos/milho'
driver.get("https://www.agrolink.com.br/cotacoes/"+sit+"")
#driver.find_element_by_xpath('//tr//td//a[@href="/cotacoes/graos/'+ sit +'"]').click()
page = requests.get(driver.current_url)
tree = html.fromstring(page.content)
produto = []
ce = []
preco = []
data = []
freq = []

extrai_info()
for aux in range(160, 162):
    p = str(aux)
    #Executa o javascript da paginacao e vai para a proxima pagina
    driver.execute_script("javascript:navigateToPage('frmFiltroGeral-5231', " + p + ")")
    test = tree.xpath('//*[@id="frmMercadoFisico-5181"]/div/span/text()')
    if len(test) == 0:
        print 'null'
    time.sleep(5)
    #ATUALIZA O HTML
    page = driver.execute_script("return document.body.innerHTML")
    tree = html.fromstring(page)
    extrai_info()

row = zip(produto, ce, preco, data, freq)
#SALVA OS VALORES RECEBIDO EM UMA LISTA
with open("csvfile", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in row:
        writer.writerow(val)
#driver.get_screenshot_as_file("capture.png")
driver.close()
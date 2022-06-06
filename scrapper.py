###################### Bibliotecas ######################

from optparse import Option
from time import sleep
import requests
import pandas as pd
import lxml

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

############ Parâmetros de config do Navegador ############

# options = Options()
# options.add_argument('--headless')
# options.add_argument('window-size=1200,900')

############### URL - Pesquisa - WebDrivers ###############

URL_BASE = 'https://www.magazineluiza.com.br'

user_search = input('O que deseja pesquisar?')

driver = webdriver.Chrome(ChromeDriverManager().install()) # webdriver + driverManager
driver.implicitly_wait(10) # 10segs
driver.get('https://www.magazineluiza.com.br/') # URL

########### Manipular o input de pesquisa do site ###########

input_search = driver.find_element_by_id('input-search') # search element by id
input_search.send_keys(user_search) # atribuo o valor ao campo de pesquisa
input_search.submit() # enter

#############################################################

sleep(5) # force wait 5segs

#### Transformar código fonte da página atual -> obj BS4 ####

result_page = driver.page_source
content = BeautifulSoup(result_page, 'lxml')

### Localizo o elemento que engloba cada anúncio de produto ###
#
### <a> ... data-testid="product-card-container" ... <a/>
  
## Pecorre e acessa os elementos filhos, coleta os dados relevantes e adiciona na lista ##

products = content.findAll('a', attrs = {'data-testid':'product-card-container'}) 
product_list = []

for product in products:

    title_prod = product.find('h2', attrs = {'data-testid':'product-title'})
    title = title_prod.text
    print('TITLE PRODUCT: ', title)

    qtd_evaluations_prod = product.find('span', attrs = {'color':'text.scratched'})
    
    if(qtd_evaluations_prod):
        qtd_evaluations = qtd_evaluations_prod.text
        print('EVALUATIONS: ', qtd_evaluations)
    else:
       qtd_evaluations = 0
       print('EVALUATIONS: ', qtd_evaluations)

    price_prod = product.find('p', attrs = {'data-testid':'price-value'})
    if(price_prod):
        price = price_prod.text
        print('PRICE: ', price) 
    else:
        price = 'Sem Estoque'
        print('PRICE: ', price)
        
    link_prod = product['href']
    link = URL_BASE + link_prod
    print('LINK: ', link)
    
    print()
    product_list.append([title, qtd_evaluations, price, link])    
    
########## Transforma a lista de listas em - DF do Pandas, converte e salva em CSV ##########
    
df_products = pd.DataFrame(product_list, columns = ['titulo_produto','quantidade_avaliacoes','preco','link'])
print(df_products)

try:
    print('Convertendo Dataframe para CSV...')
    df_products.to_csv('data-scraping.csv', index=False)
    print('CSV exportado com sucesso!')
except:
    print('Falha ao exportar CSV!')

driver.close() # or quit()

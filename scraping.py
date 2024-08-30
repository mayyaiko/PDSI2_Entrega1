import requests
from bs4 import BeautifulSoup

def scrape_menu(url: str):
    lista_textos = []
    lista_links = []

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        menu_block = soup.find('div', class_='menu-block-wrapper menu-block-2 menu-name-main-menu parent-mlid-11029 menu-level-1')
        
        if menu_block:
            ul_list = menu_block.find('ul', class_='menu nav')
            
            if ul_list:
                items = ul_list.find_all('li')
                for item in items:
                    texto = item.get_text(strip=True)
                    lista_textos.append(texto)
                    
                    link_tag = item.find('a')
                    link = "https://ufu.br" + link_tag['href'] if link_tag and 'href' in link_tag.attrs else None
                    lista_links.append(link)
            else:
                print("Não foi possível encontrar a lista UL com a classe especificada.")
        else:
            print("Não foi possível encontrar a div com a classe especificada.")
    else:
        print(f"Falha na requisição. Código de status: {response.status_code}")
    
    return lista_textos, lista_links

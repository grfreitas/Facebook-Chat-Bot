from lxml import html
import requests
from bs4 import BeautifulSoup

codigo = 'PP981511488BR'


def get_codes(words):
    # code must be in the format 'AA123456789XX'
    codes = []
    for word in words:
        if len(word) == 13:
            if word[0].isalpha() and word[6].isdigit()  and \
               word[1].isalpha() and word[7].isdigit()  and \
               word[2].isdigit() and word[8].isdigit()  and \
               word[3].isdigit() and word[9].isdigit()  and \
               word[4].isdigit() and word[10].isdigit() and \
               word[5].isdigit() and word[11].isalpha() and \
               word[12].isalpha(): codes.append(word)
    if len(codes)==0:
        return False
    else:
        return codes


def get_package_status(code)
    URL = f'http://rastreamentocorreios.info/consulta/{code}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')

    for i in range(len(soup.find_all('li'))):

        data = soup.find_all('li')[i].get_text('|').split('|')
        
        if ' ' in data: 
            data.remove(' ')
        if 'De' in data:
            data.remove('De')
        if 'Para' in data:
            data.remove('Para')
            
        data = data[:-1]
        
        updated_at = data[0]
        status     = data[1].strip().title()
        
        if status == 'Objeto Encaminhado':
            start = data[2].strip()
            end   = data[3].strip()
            response = f'{updated_at}\n{status}\nDe: {start}\nPara: {end}'

        elif status == 'Objeto Postado':
            start = data[2].strip()
            response = f'{updated_at}\n{status}\nDe: {start}'

        else: 
            response = 'Ops, não sei como lidar com esse status.'
        
        responses.append(response)

    return responses


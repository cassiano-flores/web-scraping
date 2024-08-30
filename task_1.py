# coding=utf-8
import os
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = 'http://127.0.0.1:8000'
INDEX_URL = BASE_URL + '/places/default/index/'
CSV_FILE = 'countries_data.csv'
COUNTRY_DATA = []
INDEX_COUNTRY = 0
FILE_EXISTS = os.path.isfile(CSV_FILE)


# Função para processar as páginas de países a partir de um índice
def process_country_pages(index_url):
    global COUNTRY_DATA, INDEX_COUNTRY

    is_empty = True
    response = requests.get(index_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrando todos os links para os países
    country_links = soup.find_all('a', href=True)
    for link in country_links:
        if 'view' in link['href']:  # Verifica se o link é para uma página de país
            is_empty = False
            country_url = BASE_URL + link['href']
            print('Acessando: ' + country_url)

            country_data_new = get_country_data(country_url)
            country_data_current = country_data_new

            if FILE_EXISTS:
                country_data_old = get_country_data_old()
                country_data_current = country_data_old[INDEX_COUNTRY]

                for key in country_data_current:
                    if key != 'timestamp':
                        if country_data_current[key] != country_data_new[key]:
                            country_data_current = country_data_new
                            break

            COUNTRY_DATA.append(country_data_current)
            INDEX_COUNTRY += 1

    return is_empty


def get_country_data_old():
    country_data_old = []

    with open(CSV_FILE, mode='r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        for row in reader:
            # Para evitar o problema das linhas em branco
            if row['country'].strip():
                country_data_old.append(row)

    return country_data_old


# Função para capturar o HTML das páginas de países
def get_country_data(country_url):
    response = requests.get(country_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraindo os dados do país usando IDs e classes fornecidas
    country_name = soup.find('tr', id='places_country__row').find('td', class_='w2p_fw').text.strip()
    currency_name = soup.find('tr', id='places_currency_name__row').find('td', class_='w2p_fw').text.strip()

    continent_link = soup.find('tr', id='places_continent__row').find('td', class_='w2p_fw').a['href']
    continent_name = get_continent_name(BASE_URL + continent_link)

    neighbours_row = soup.find('tr', id='places_neighbours__row')
    neighbours_links = [a['href'] for a in neighbours_row.find_all('a')]
    neighbours = [get_neighbour_name(BASE_URL + link) for link in neighbours_links]
    neighbours_names = ', '.join(neighbours)

    # Retornando os dados extraídos
    return {
        'country': country_name,
        'currency': currency_name,
        'continent': continent_name,
        'neighbours': neighbours_names,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def get_continent_name(continent_url):
    response = requests.get(continent_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find('h2').text.strip()


def get_neighbour_name(neighbour_url):
    response = requests.get(neighbour_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    neighbour_row = soup.find('tr', id='places_country__row')
    if neighbour_row:
        return neighbour_row.find('td', class_='w2p_fw').text.strip()
    else:
        return ''


def write_csv():
    # Abre o arquivo CSV para leitura e escrita
    with open(CSV_FILE, mode='w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['country', 'currency', 'continent', 'neighbours', 'timestamp'],
                                delimiter=';')
        # Cabeçalho
        writer.writeheader()

        for i in range(len(COUNTRY_DATA)):
            writer.writerow(COUNTRY_DATA[i])


def is_different(existing_row, new_data):
    data_to_check = ['country', 'currency', 'continent', 'neighbours']
    for field in data_to_check:
        if existing_row[field] != new_data[field]:
            return True
    return False


def main():
    index = 0
    while True:
        index_url = INDEX_URL + str(index)
        print('Navegando para o índice: ' + index_url)
        if process_country_pages(index_url):
            write_csv()
            break
        else:
            index += 1


if __name__ == "__main__":
    main()

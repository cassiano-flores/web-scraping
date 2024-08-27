# coding=utf-8
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

BASE_URL = 'http://127.0.0.1:8000/'
INDEX_URL = BASE_URL + 'places/default/index/'
MIN_INDEX = 0
MAX_INDEX = 26


# Função para capturar o HTML das páginas de países
def get_country_data(country_url):
    response = requests.get(country_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraindo os dados do país usando IDs e classes fornecidas
    country_name = soup.find(id='places_country__row').find(class_='w2p_fw').text.strip()
    currency_name = soup.find(id='places_currency_name__row').find(class_='w2p_fw').text.strip()
    continent_name = soup.find(id='places_continent__row').find(class_='w2p_fw').text.strip()

    # Extraindo os vizinhos
    neighbours = []
    neighbours_links = soup.find_all('a', href=True, class_='w2p_fw')
    for neighbour_link in neighbours_links:
        if 'view' in neighbour_link['href']:
            # Aqui temos o link, então precisamos acessar a página do vizinho para obter o nome completo do país
            neighbour_url = BASE_URL + neighbour_link['href']
            neighbour_response = requests.get(neighbour_url)
            neighbour_soup = BeautifulSoup(neighbour_response.text, 'html.parser')
            neighbour_name = neighbour_soup.find(id='places_country__row').find(class_='w2p_fw').text.strip()
            neighbours.append(neighbour_name)

    # Retornando os dados extraídos
    return {
        'country': country_name,
        'currency': currency_name,
        'continent': continent_name,
        'neighbours': ', '.join(neighbours),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


# Função para processar as páginas de países a partir de um índice
def process_country_pages(index_url):
    response = requests.get(index_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrando todos os links para os países
    country_links = soup.find_all('a', href=True)

    for link in country_links:
        if 'view' in link['href']:  # Verifica se o link é para uma página de país
            country_url = BASE_URL + link['href']
            print('Acessando: ' + country_url)
            country_data = get_country_data(country_url)

            # Escrever os dados no CSV
            # ------------------------------------------
            # if não existe or dados_diferentes:
            # ------------------------------------------
            with open('countries_data.csv', 'a') as csvfile:
                fieldnames = ['country', 'currency', 'continent', 'neighbours', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

                # Escreve o cabeçalho se o arquivo estiver vazio
                csvfile.seek(0, 2)  # Move o cursor para o final do arquivo
                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(country_data)


# ------------------------------------------
# tornar uma forma de fazer isso consistentemente (monitorar continuamente)
# ------------------------------------------
# Navegando pelos diferentes índices
for index in range(MIN_INDEX, MAX_INDEX):
    index_url = INDEX_URL + str(index)
    print('Navegando para o índice: ' + index_url)
    process_country_pages(index_url)


# ------------------------ TAREFA 1 ------------------------
# python web2py.py
# https://www.youtube.com/watch?v=QiyJh-bl-oE
# 1. Faça um crawler capaz de navegar por todas as páginas de países e acessar seus HTML

# 2. Faça scraping dos HTMLs das páginas para armazenar os seguintes dados dos países em um arquivo CSV:
# a. Nome do país (campo country)
# b. Nome da moeda (campo currency name)
# c. Nome do continente que pertence (campo continente)
# d. Nome de todos os países vizinhos (campo neighbours - Atenção, é o NOME e não a sigla!)
# e. Salvar uma coluna extra no csv contendo um timestamp do momento no qual os dados foram obtidos.

# 3. Faça um crawler que monitore as páginas de países e procure por atualizações.
# Caso algum registro tenha sido atualizado desde sua obtenção, esse registro deve ser atualizado
# no arquivo CSV, caso contrário manter a versão anterior.
# ----------------------------------------------------------

# ------------------------ TAREFA 2 ------------------------
# https://www.imdb.com/
# 1. Faça scraping para obter os filmes presentes no Calendário de Lançamentos do IMDB.
# Devem ser obtidos: Título, Data de Lançamento, Gênero(s) e o link para página da série.

# 2. Faça scraping das páginas específicas dos filmes obtidos no item anterior.
# Obtenha dessa página o(s) nome(s) do(s) diretor(es) e a lista dos atores presentes no elenco principal (Não é a lista completa de atores!).

# 3. Salve as informações obtidas em um arquivo de tipo JSON.
# ----------------------------------------------------------

# ------------------------ TAREFA 3 ------------------------
# Cada aluno deve elaborar um relatório descrevendo a sua participação no desenvolvimento do trabalho,
# as tecnologias utilizadas para resolver as tarefas e as facilidades e dificuldades encontradas.
# Além disso o aluno também deve descrever a sua percepção sobre a participação dos colegas no trabalho.
# A entrega deve ser em formato de relatório, contendo título e nome do aluno.
# ----------------------------------------------------------

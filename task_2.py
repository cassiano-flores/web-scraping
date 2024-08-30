# coding=utf-8
import os
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = 'https://www.imdb.com'
CALENDAR_URL = BASE_URL + '/calendar/'
MOVIE_URL = BASE_URL + '/title/'
CSV_FILE = 'movies_data.csv'
FILE_EXISTS = os.path.isfile(CSV_FILE)



def get_movie_data():
    return ''





def main():
    index = 0
    # while True:
    #     index_url = INDEX_URL + str(index)
    #     print('Navegando para o índice: ' + index_url)
    #     if process_country_pages(index_url):
    #         write_csv()
    #         break
    #     else:
    #         index += 1


if __name__ == "__main__":
    main()

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

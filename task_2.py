# coding=utf-8
import io
import json
import os
import requests
from collections import OrderedDict
from bs4 import BeautifulSoup

BASE_URL = 'https://www.imdb.com'
CALENDAR_URL = BASE_URL + '/calendar/'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
JSON_FILE = 'movies_data.json'
FILE_EXISTS = os.path.isfile(JSON_FILE)


def get_movies_data(releases_url):
    response = requests.get(releases_url, headers=HEADERS)

    # Procurando o JSON na resposta (simplesmente usando split para extrair)
    json_start = response.text.find('{"props"')
    json_end = response.text.find('</script>', json_start)
    json_data = response.text[json_start:json_end]

    # Carregando o JSON em um objeto Python
    data = json.loads(json_data)

    # Navegando pelo JSON para extrair os dados dos filmes
    movies_data = []
    for group in data['props']['pageProps']['groups']:
        for entry in group['entries']:
            movie = {
                "title": entry['titleText'],
                "genres": entry['genres'],
                "release_date": entry['releaseDate'],
                "link": "https://www.imdb.com/title/" + entry['id']
            }
            movie_details = get_movie_details(movie['link'])
            movie.update(movie_details)

            # Adiciona o dicionário atualizado à lista de filmes
            movies_data.append(movie)

    key_order = ['title', 'release_date', 'link', 'genres', 'directors', 'cast']
    ordered_movies_data = [
        OrderedDict((key, movie[key]) for key in key_order)
        for movie in movies_data
    ]

    return ordered_movies_data


def get_movie_details(movie_url):
    response = requests.get(movie_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extrai o(s) nome(s) do(s) diretor(es)
    directors = []
    for director in soup.find_all('a', href=lambda href: href and 'tt_ov_dr' in href):
        directors.append(director.text.strip())

    # Extrai os principais atores (cast)
    cast = []
    for actor in soup.find_all('a', href=lambda href: href and 'tt_cl_t' in href)[:5]:
        cast.append(actor.text.strip())

    directors = list(set(directors))
    cast = list(set(cast))

    return {
        'directors': directors,
        'cast': cast
    }


def write_json(data):
    with io.open(JSON_FILE, 'w', encoding='utf-8') as file:
        file.write(unicode(json.dumps(data, ensure_ascii=False, indent=4)))


def main():
    movies_data = get_movies_data(CALENDAR_URL)
    write_json(movies_data)


if __name__ == "__main__":
    main()

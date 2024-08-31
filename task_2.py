import io
import json
import requests
from collections import OrderedDict
from bs4 import BeautifulSoup

BASE_URL = 'https://www.imdb.com'
CALENDAR_URL = BASE_URL + '/calendar/'
JSON_FILE = 'movies_data.json'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}


def get_movies_data(releases_url):
    response = requests.get(releases_url, headers=HEADERS)

    # proccura json na resposta (nao deu pra utilizar soup direto)
    json_start = response.text.find('{"props"')
    json_end = response.text.find('</script>', json_start)
    json_data = response.text[json_start:json_end]

    # carrega json
    data = json.loads(json_data)

    # navega pelo json e extrai os dados dos filmes
    movies_data = []
    for group in data['props']['pageProps']['groups']:
        # obtem os dados dos filmes, primeiro passo
        for entry in group['entries']:
            movie = {
                "title": entry['titleText'],
                "genres": entry['genres'],
                "release_date": entry['releaseDate'],
                "link": "https://www.imdb.com/title/" + entry['id']
            }
            # obtem os detalhes do filme, segundo passo
            movie_details = get_movie_details(movie['link'])
            movie.update(movie_details)

            # adiciona ao dicionario ja com detalhes (diretor e atores)
            movies_data.append(movie)

    # ordena propriedades
    key_order = ['title', 'release_date', 'link', 'genres', 'directors', 'cast']
    ordered_movies_data = [
        OrderedDict((key, movie[key]) for key in key_order)
        for movie in movies_data
    ]

    return ordered_movies_data


def get_movie_details(movie_url):
    print('acessando: ' + movie_url)
    response = requests.get(movie_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # extrai diretores
    directors = []
    for director in soup.find_all('a', href=lambda href: href and 'tt_ov_dr' in href):
        directors.append(director.text.strip())

    # extrai principais atores
    cast = []
    for actor in soup.find_all('a', href=lambda href: href and 'tt_cl_t' in href)[:5]:
        cast.append(actor.text.strip())

    # remove duplicados
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

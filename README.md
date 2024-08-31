# Trabalho 1 - Web Scraping

**Nome:** Cassiano Luis Flores Michel  
**Matrícula:** 20204012-7

## Descrição do Projeto

Este projeto contém duas tarefas principais desenvolvidas em Python 2.7:

1. **Task 1 (`task_1.py`)**: Realiza scraping de dados de páginas HTML, em um site rodando localmente, sobre países e
   salva os dados extraídos em um arquivo `countries_data.csv`.
2. **Task 2 (`task_2.py`)**: Realiza scraping de dados de páginas HTML, em uma página do IMDB, sobre países e salva os
   dados de filmes em um arquivo `movies_data.json`.

## Requisitos

- Python 2.7
- Bibliotecas Python:
    - `os`
    - `io`
    - `csv`
    - `json`
    - `requests`
    - `datetime`
    - `collections`
    - `BeautifulSoup`

## Como Rodar as Tarefas

### Task 1: Extração de Dados de Países

1. Abra o terminal na pasta do projeto.
2. Execute o script `task_1.py`:
   ```bash
   python task_1.py
   ```
3. O script irá realizar o scraping dos dados e salvar o resultado em um arquivo chamado `countries_data.csv`.

#### Exemplo de Resultados Esperados

O arquivo `countries_data.csv` conterá os seguintes dados:

```
country;currency;continent;neighbours;timestamp
Afghanistan;Afghani;Asia;Turkmenistan, China, Iran, Tajikistan, Pakistan, Uzbekistan;2024-08-29 00:52:20
Aland Islands;Euro;Europe;;2024-08-29 00:52:20
...
```

### Task 2: Organização de Dados de Filmes

1. Abra o terminal na pasta do projeto.
2. Execute o script `task_2.py`:
   ```bash
   python task_2.py
   ```
3. O script irá organizar os dados de filmes e salvar o resultado em um arquivo chamado `movies_data.json`.

#### Exemplo de Resultados Esperados

O arquivo `movies_data.json` conterá os seguintes dados:

```json
[
  {
    "title": "Os Fantasmas Ainda se Divertem - Beetlejuice Beetlejuice",
    "release_date": "Thu, 05 Sep 2024 00:00:00 GMT",
    "link": "https://www.imdb.com/title/tt2049403",
    "genres": [
      "Comedy",
      "Fantasy",
      "Horror"
    ],
    "directors": [
      "Tim Burton"
    ],
    "cast": [
      "Justin Theroux",
      "Winona Ryder",
      "Catherine O'Hara",
      "Jenna Ortega",
      "Michael Keaton"
    ]
  },
  ...
]
```

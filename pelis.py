import os
import sys
import re
import requests
from bs4 import BeautifulSoup


CSVFILE = "pelis.csv"
LOG = []

URL_SEARCH_FILMAFFINITY = "https://www.filmaffinity.com/es/search.php?stype=title&stext="

USER_AGENT = "Mozilla/5.0 (iPad; CPU OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
STATUS_CODE_OK = 200
STATUS_CODE_NOT_FOUND = 404
STATUS_CODE_ERROR = 502

# MOVE_TO_YEAR = True
MOVE_TO_YEAR = False
SEPARATOR = "\t"

def web_scrapping_filmaffinity_main_page(htmlText):
    soup = BeautifulSoup(htmlText, "html.parser")
    # Title
    title = None
    try:
        title = soup.find('h1').find('span').get_text().strip()
    except:
        title = ""

    # URL
    allLinks = soup.find_all('a')
    url = None
    for link in allLinks:
        if 'Ficha' in link.get_text():
            url = link['href']
            break

    # Rating
    rating = None
    try:
        rating = soup.find(id="movie-rat-avg").get_text().replace("  ", "").strip()
    except:
        rating = "--"

    # Image
    image = soup.find('a', class_="lightbox")['href']

    dtElements = soup.find_all('dt')
    ddElements = soup.find_all('dd')
    data = {}
    for dt, dd in zip(dtElements, ddElements):
        key = dt.text
        value = dd.text
        data[key] = value

    # Original Title
    originalTitle = None
    try:
        originalTitle = data["Título original"].strip().replace(".", ",")
    except:
        originalTitle = ""

    # Year
    year = None
    try:
        year = data["Año"].strip()
    except:
        year = ""

    # Country
    country = None
    try:
        country = data["País"].strip()
    except:
        country = ""

    # Directors
    director = None
    try:
        director = data["Dirección"].strip()
    except:
        director = ""

    # Genre
    genre = None
    try:
        genre = re.sub(r'\s+', ' ', re.sub(r'\s*\|\s*', '. ', data["Género"])).strip()
    except:
        genre = ""

    # Company
    company = None
    try:
        company = data["Compañías"].strip()
    except:
        company = ""

    # Summary
    summary = None
    try:
        summary = data["Sinopsis"].strip()
    except:
        summary = ""

    # Cast
    cast = None
    try:
        castElement = soup.find('dd', class_="card-cast-debug")
        castArray = castElement.find_all('a')
        names = [a.get('title') for a in castArray if a.get('title')]
        cast = ", ".join(names)
    except:
        cast = ""

    # Credits
    credits = None
    try:
        credits = data["Guion"].strip()
    except:
        credits = ""

    # Photography
    photography = None
    try:
        photography = data["Fotografía"].strip()
    except:
        photography = ""

    # Music
    music = None
    try:
        music = data["Música"].strip()
    except:
        music = ""

    # Rating count
    ratingCount = None
    try:
        ratingCountElement = soup.find(id="movie-count-rat")
        ratingCount = ratingCountElement.find('span')['content']
    except:
        ratingCount = "0"

    # Duration
    duration = None
    try:
        duration = data["Duración"].strip().replace(".", "")
    except:
        duration = ""

    return [title, url, rating, year, image, originalTitle, country, director, genre, company, summary, cast, credits,
            photography, music, ratingCount, duration]

def web_scrapping_filmaffinity_search_page(htmlText):
    soup = BeautifulSoup(htmlText, "html.parser")
    # Encontrar todas las etiquetas con clase 'mc-title'
    filmaffinityRawElements = soup.find_all(class_='movie-card mc-flex movie-card-1')

    # Crear una lista para almacenar los datos de los elementos encontrados
    filmaffinityElements = []

    # Comprobamos si no hay resultados
    noResults = soup.find('b', string=re.compile(r"No hay resultados?"))

    # Extraer títulos y URLs de las películas y agregar a la lista
    if noResults:
        return filmaffinityElements
    elif filmaffinityRawElements:  # Hemos ido a la pantalla de búsqueda porque hay más de un resultado
        for filmElement in filmaffinityRawElements:
            # Image
            posterElement = filmElement.find('div', class_="mc-poster")

            # URL
            linkOnImage = posterElement.find('a')
            url = linkOnImage['href']

            # Title
            title = linkOnImage['title'].rstrip()

            # Year
            yearElement = filmElement.find_previous(class_='ye-w')
            year = yearElement.get_text() if yearElement else '-'

            # Rating
            ratingElement = posterElement.find_next(class_='avgrat-box')
            rating = ratingElement.get_text() if ratingElement else '--'

            filmaffinityElements.append([title, url, rating, year])
    else:  # No hemos ido a la pantalla de búsqueda sino a la página de la película/serie en sí
        completeInformation = web_scrapping_filmaffinity_main_page(htmlText)
        filmaffinityElements.append(
            [completeInformation[0], completeInformation[1], completeInformation[2], completeInformation[3],
             completeInformation[4]])
    return filmaffinityElements


def url_to_film_code(url):
    numeroPelicula = re.search(r'film(\d+)\.html', url)
    if numeroPelicula:
        numeroPelicula = numeroPelicula.group(1)
        return numeroPelicula
    else:
        raise ValueError(f'No se encontró un número de película en el enlace: {url}')


def obtener_ano_pelicula(titulo):
    headers = {"user-agent": USER_AGENT}

    url = f'{URL_SEARCH_FILMAFFINITY}{titulo}'
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        elements = web_scrapping_filmaffinity_search_page(response.text)

        if not elements:
            return False
        years = []
        # print(elements)
        for element in elements:
            if element[3] == "":
                continue
            if element[0].lower() != titulo.lower():
                continue
           
            anio = int(element[3])
            if anio>2022:
                continue
            years.append(anio)
        return years

    return False


def scan_directories(root_dir):
    extensions = (".srt", ".txt", ".csv")
    patron = r"^(.*?)(?:\s*\((\d{4})\))?$"

    for curdir, subdirs, files in os.walk(root_dir):
        for file in files:
            if not file.lower().endswith(extensions):
                year = ""
                peli, ext = os.path.splitext(file)
                match = re.match(patron, peli)
                loc = os.path.join(curdir, file)
                if match:
                    peli = match.group(1).strip()
                    year = match.group(2)
                if year is None:
                    print(f"Buscando año de {peli}:")
                    years = obtener_ano_pelicula(peli)

                    if years:
                        print(years)
                        if isinstance(years, list) and len(years)==1:
                            year = str(years[0])
                            if MOVE_TO_YEAR:
                                file_name = f"{year}/{peli} ({year}){ext}"
                                if not os.path.isdir(os.path.join(curdir, year)):
                                    os.mkdir(os.path.join(curdir, year))
                            else:
                                file_name = f"{peli} ({year}){ext}"
                            newloc = os.path.join(curdir, file_name)

                            os.rename(loc, newloc)

                else:
                    if not year in curdir and MOVE_TO_YEAR:
                        newloc = os.path.join(curdir, year, file)
                        if not os.path.isdir(os.path.join(curdir, year)):
                            os.mkdir(os.path.join(curdir, year))
                        os.rename(loc, newloc)
                        loc = newloc
                if year is None:
                    year = ""
                LOG.append(f"{peli}{SEPARATOR}{year}{SEPARATOR}{ext}{SEPARATOR}{loc}")


def main():
    print("")
    if len(sys.argv) > 1:
        origen = sys.argv[1]
    else:
        origen = os.getcwd()

    if origen == "":
        origen = os.getcwd()
    if origen[-1] != "\\":
        origen += "\\"

    print(f"Buscando pelis en {origen}")
    print("")
    LOG.append(f"Película{SEPARATOR}Año{SEPARATOR}Extensión{SEPARATOR}Fichero")

    # year = obtener_ano_pelicula("Ant Man 2")
    # print(year)
    # print(type(year))
    # print(len(year))
    #
    scan_directories(origen)

    logc = "\n".join(LOG)
    with open(CSVFILE, "w", encoding="UTF-8") as pelis:
        pelis.write(logc)

    #print("")
    #print("Finalizado")
    #print("")

    #endd = input("Presiona Intro para salir.")


if __name__ == "__main__":
    main()

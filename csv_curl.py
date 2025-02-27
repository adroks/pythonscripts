import os
import sys
import csv
import requests
import re


def main():
    print("")
    # if len(sys.argv) > 1:
    #     csv_file_path = sys.argv[1]
    # else:
    #     csv_file_path = input("Introduce la ruta del fichero: ")

    csv_file_path = "C:\\Users\\adrok\\Downloads\\proyectos\\fisan\\urls.txt"
    posts_path = "C:\\Users\\adrok\\Downloads\\proyectos\\fisan\\sp22ir_posts.csv"
    permalinks_path = "C:\\Users\\adrok\\Downloads\\proyectos\\fisan\\permalinks.csv"
    htaccess_file_path = "F:\\IDI\\fisan.com\\.htaccess"

    if os.path.isfile(csv_file_path) and os.path.isfile(htaccess_file_path) and os.path.isfile(posts_path):
        with open(htaccess_file_path, encoding='utf-8') as htaccess:
            htaccess_file = htaccess.read().splitlines()

        with open(permalinks_path, encoding='utf-8') as permalinks_handler:
            permalinks_csv = list(csv.DictReader(permalinks_handler, delimiter=","))

        with open(posts_path, encoding='utf-8') as posts_handler:
            posts_csv = list(csv.DictReader(posts_handler, delimiter=","))

        with open(csv_file_path, encoding='utf-8') as csv_file_handler:
            lines = csv_file_handler.read().splitlines()

            for row in lines:
                if row == "":
                    continue
                htas = row.replace("https://www.fisan.com/", "301 ^/")
                hta = f"{htas}$"

                lista_nueva = [x for x in htaccess_file if hta in x]
                if len(lista_nueva)>0:
                    print(lista_nueva)
                    for l in lista_nueva:
                        htaccess_file.remove(l)
                hta = f"{htas}?"
                lista_nueva = [x for x in htaccess_file if hta in x]
                if len(lista_nueva)>0:
                    print(lista_nueva)
                    for l in lista_nueva:
                        htaccess_file.remove(l)

                resp = requests.get(row, allow_redirects=False)
                if resp.status_code == 301:
                    print(f"{resp.status_code}: {row} to {resp.headers['location']}")
                    loc = resp.headers['location'].replace("https://www.fisan.com/", "")[:-1]
                    for pl in permalinks_csv:
                        if pl['permalink']==loc:
                            for p in posts_csv:
                                if p['id']==pl['id']:
                                    slug = os.path.basename(os.path.normpath(row))
                                    if p['url']==slug:
                                        print(slug)
                                        lines.remove(row)

                elif resp.status_code == 200 or resp.status_code == 404:
                    print(f"{resp.status_code}: {row}")
                    lines.remove(row)
                else:
                    print(f"{resp.status_code}: {row}")


            with open(csv_file_path, 'w', encoding='utf-8') as output:
                for row in lines:
                    if row == "":
                        continue
                    output.write(str(row) + '\n')
            with open(htaccess_file_path, 'w', encoding='utf-8') as output:
                for row in htaccess_file:
                    output.write(str(row) + '\n')

if __name__ == "__main__":
    main()

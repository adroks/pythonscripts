import os
import sys
import csv
import json


def csv_to_json(csv_file_path, json_file_path, delimiter):
    data_dict = {}
    with open(csv_file_path, encoding='utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler, delimiter=delimiter)
        data_dict = [row for row in csv_reader]

    with open(json_file_path, 'w', encoding='utf-8') as json_file_handler:
        json_file_handler.write(json.dumps(data_dict, indent=4))
        print(f"Guardado {json_file_path}")


def main():
    print("")
    if len(sys.argv) > 1:
        csv_file_path = sys.argv[1]
    else:
        csv_file_path = input("Introduce la ruta del fichero: ")
    if len(sys.argv) > 2:
        delimiter = sys.argv[2]
    else:
        delimiter = input("¿Separado por? (,): ")
    if not delimiter:
        delimiter = ","

    if os.path.isfile(csv_file_path):
        pre, ext = os.path.splitext(csv_file_path)
        json_file_path = pre + ".json"
        csv_to_json(csv_file_path, json_file_path, delimiter)

    # input("Presiona Intro para salir.")


if __name__ == "__main__":
    main()

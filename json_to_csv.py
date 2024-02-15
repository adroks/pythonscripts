import os
import sys
import pandas as pd
import json


def json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, encoding='utf-8') as json_file_handler:
        df = pd.read_json(json_file_handler)
        df.to_csv(csv_file_path, encoding='utf-8', index=False)
        print(f"Guardado {csv_file_path}")


def main():
    print("")
    if len(sys.argv) > 1:
        json_file_path = sys.argv[1]
    else:
        json_file_path = input("Introduce la ruta del fichero: ")

    if os.path.isfile(json_file_path):
        pre, ext = os.path.splitext(json_file_path)
        csv_file_path = pre + ".csv"
        json_to_csv(json_file_path, csv_file_path)


if __name__ == "__main__":
    main()

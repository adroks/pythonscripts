import zipfile
import os
import sys
import datetime



print("")
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = input("Introduce la ruta del fichero: ")

parent = os.path.dirname(os.path.realpath(file_path))
data = open(file_path, "r", encoding="utf8").read()

files = data.split("\n")
archivo_zip = os.path.join(parent, "deploy_" + datetime.datetime.now().strftime('%Y_%m_%d') + ".zip")

with zipfile.ZipFile(archivo_zip, "w") as zipf:
    for file in files:
        file = file.strip()
        file_path = os.path.join(parent, file)
        if os.path.isfile(file_path):
            print(file)
            zipf.write(file_path, file)

print("")
print(f"Creado {archivo_zip}")
print("")

input("Presiona Intro para salir.")
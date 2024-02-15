import os
import sys


def delete_directories(root_dir):
    empty = False
    for curdir, subdirs, files in os.walk(root_dir):
        if len(subdirs) == 0 and len(files) == 0:
            print('Empty directory: {}'.format(curdir))
            os.rmdir(curdir)
            empty = True
        # elif len(subdirs) > 0 and len(files) > 0:
        #     print('Used directory: {}'.format(curdir))
    return empty

def main():
    print("")
    if len(sys.argv) > 1:
        origen = sys.argv[1]
    else:
        origen = input("Introduce la ruta a eliminar (intro para carpeta actual): ")

    if origen == "":
        origen = os.getcwd()
    if origen[-1] != "\\":
        origen += "\\"

    print(f"Buscando carpetas vacías en {origen}")
    print("")

    while delete_directories(origen):
        print("")

    print("")
    print("Finalizado")
    print("")

    endd = input("Presiona Intro para salir.")


if __name__ == "__main__":
    main()

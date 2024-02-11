import os
import sys
from PIL import Image


# print(os.path.dirname(sys.executable))


def resize_images(root_dir, ancho, alto):

    files = [f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, f))]
    extensions = (".jpg", ".png", ".gif")

    if not files:
        print(f"Carpeta vacía")
    else:
        if ancho == "":
            ancho = input("Introduce el ANCHO del thumbnail: ")
        if alto == "":
            alto = input("Introduce el ALTO del thumbnail: ")
        folder = None
        while folder is None:
            folder = input("¿Crear carpeta /thumbs? S/N (por defecto SI): ")
            if folder == "" or folder.lower() == "s":
                folder = True
            elif folder.lower() == "n":
                folder = False
            else:
                folder = None
                print("Introduce una respuesta válida.")

        if ancho.isdigit() and alto.isdigit():
            print("")
            if folder:
                thumb_folder = os.path.join(root_dir, "thumbs")
                if not os.path.isdir(thumb_folder):
                    os.mkdir(thumb_folder)
            else:
                thumb_folder = root_dir
            for filename in files:
                if filename.lower().endswith(extensions):
                    print(filename)
                    image = Image.open(os.path.join(root_dir, filename))
                    # if int(ancho) < image.size[0] or int(alto) < image.size[1]:
                    print(f" Original size : {image.size[0]} x {image.size[1]}")

                    image.thumbnail((int(ancho), int(alto)))
                    if folder:
                        dest_name = filename
                    else:
                        dest_name = "{0}_{2}.{1}".format(
                            *filename.rsplit('.', 1) + [f"{image.size[0]}x{image.size[1]}"])
                    dest_path = os.path.join(thumb_folder, dest_name)
                    print(f" Final size : {image.size[0]} x {image.size[1]}")
                    image.save(dest_path, subsampling=0, quality=95)
                    # else:
                    #     print(" Sin cambios.")
        else:
            print("")
            print(f"Dimensiones erróneas")


def main():
    print("")

    origen = sys.argv[1] if len(sys.argv) > 1 else input("Introduce la ruta (intro para carpeta actual): ")
    ancho = sys.argv[2] if len(sys.argv) > 2 else ""
    alto = sys.argv[3] if len(sys.argv) > 3 else ""

    if origen == "":
        origen = os.getcwd()
    if origen[-1] != "\\":
        origen += "\\"

    print(f"Buscando imágenes en {origen}")
    print("")
    resize_images(origen, ancho, alto)

    print("")
    # print("Finalizado")
    # print("")

    # endd = input("Presiona Intro para salir.")


if __name__ == "__main__":
    main()

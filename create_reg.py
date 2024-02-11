import os
import sys
import json

print("")

prefix = input("Introduce el PREFIJO: (adk_)")
if prefix == "":
    prefix = "adk_"
else:
    prefix += "_"

exec_path = sys.executable.replace("\\", "\\\\")
curr_path = os.getcwd().replace("\\", "\\\\")
iconfile = os.path.join(os.getcwd(), "favicon.ico").replace("\\", "\\\\")

f = open('registro.json', encoding="UTF-8")
registro = json.load(f)

f = open("registro.reg", "w", encoding="iso-8859-1")
f.write("Windows Registry Editor Version 5.00\n")
f.write("\n")

for row in registro:
    key = f"{row['path']}\{row['file']}"
    if 'text' in row:
        key = f"{row['path']}\{prefix}{row['file']}"
    f.write(f"[{key}]\n")
    if 'text' in row:
        f.write(f"@=\"{row['text']}\"\n")
        f.write(f"\"icon\"=\"{iconfile}\"\n")
    if 'command' in row:
        f.write("\n")
        f.write(f"[{key}\command]\n")
        f.write(f"@=\"{exec_path} {curr_path}\\\\{row['file']}.py \\\"{row['command']}\\\"\"\n")

    f.write("\n")

print("Fichero de registro creado.")
f.close()

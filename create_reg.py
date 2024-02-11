import os
import sys
import json

print("")

print(sys.executable)

exec_path = sys.executable.replace("\\", "\\\\")
curr_path = os.getcwd().replace("\\", "\\\\")
iconfile = os.path.join(os.getcwd(), "icono.ico").replace("\\", "\\\\")

f = open('registro.json')
registro = json.load(f)


f = open("registro.reg", "w")
f.write("Windows Registry Editor Version 5.00\n")
f.write("\n")

for row in registro:
    f.write(f"[{row['path']}\{row['file']}]\n")
    if 'text' in row:
        f.write(f"@=\"{row['text']}\"\n")
        f.write(f"\"icon\"=\"{iconfile}\"\n")
    if 'command' in row:
        f.write("\n")
        f.write(f"[{row['path']}\{row['file']}\command]\n")
        f.write(f"@=\"{exec_path} {curr_path}\\\\{row['file']}.py \\\"{row['command']}\\\"\"\n")

    f.write("\n")

print("Fichero de registro creado.")
f.close()

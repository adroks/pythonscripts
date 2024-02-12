import os
import sys
import json
import winreg


def set_reg_value(path, name="", value=""):
    try:
        winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, path)
        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


def set_reg_key(path, key="", value=""):
    try:
        winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, path)
        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, path, 0, winreg.KEY_WRITE)
        winreg.SetValue(registry_key, key, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


print("")
prefix = "adk_"

exec_path = sys.executable
curr_path = os.getcwd()
icon_name = os.path.join(os.getcwd(), "favicon.ico")

f = open('registro.json', encoding="UTF-8")
registro = json.load(f)

for row in registro:
    srk = set_reg_key(f"{row['path']}", f"{prefix}{row['file']}", row['text'])
    if srk:
        key = f"{row['path']}\{prefix}{row['file']}"
        set_reg_value(key, "icon", icon_name)
        if 'command' in row:
            py_path = os.path.join(curr_path, f"{row['file']}.py")
            set_reg_key(f"{key}", "command", f"{exec_path} {py_path} \"{row['command']}\"")
        print(f"Añadido al registro: {key}")

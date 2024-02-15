import os
import sys
import json
import winreg


def set_reg_value(key, path, name="", value=""):
    try:
        winreg.CreateKey(key, path)
        registry_key = winreg.OpenKey(key, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


def set_reg_key(key, path, key_name="", value=""):
    try:
        winreg.CreateKey(key, path)
        registry_key = winreg.OpenKey(key, path, 0, winreg.KEY_WRITE)
        winreg.SetValue(registry_key, key_name, winreg.REG_SZ, value)
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
    key = winreg.HKEY_CLASSES_ROOT

    srk = set_reg_key(key, f"{row['path']}", f"{prefix}{row['file']}", row['text'])
    if srk:
        path = f"{row['path']}\{prefix}{row['file']}"
        set_reg_value(key, path, "icon", icon_name)
        if 'command' in row:
            py_path = os.path.join(curr_path, f"{row['file']}.py")
            set_reg_key(key,f"{path}", "command", f"{exec_path} {py_path} \"{row['command']}\"")
        print(f"Añadido al registro: {path}")

import requests
import zipfile
import os
import shutil
import win32api
import sys
import winshell
from pathlib import Path
from swinlnk.swinlnk import SWinLnk

###| Baixa o arquivo |###
url = "https://github.com/Maulem/Manga-Checker/archive/refs/heads/main.zip"
request = requests.get(url, allow_redirects=True)

###| Diretorios |###
home_dir  = os.path.expanduser("~")
temp_dir  = home_dir + "/AppData/Roaming/temp-manga-checker"
final_dir = home_dir + "/AppData/Roaming/Manga Checker"
zipped = temp_dir + "/Manga Checker.zip"
multi_file_folder = temp_dir + "/Manga-Checker-main/exe/multi-file"
exe_file = final_dir + "/Manga Checker.exe"
desktop = str(Path(winshell.desktop()))
shortcut_file = desktop + "/Manga Checker.lnk"


###| Cria a pasta temp |###
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)
else:
    try:
        shutil.rmtree(temp_dir)
    except:
        pass
    sys.exit()

###| Cria o arquivo .zip |###
open(zipped, 'wb').write(request.content)

###| Extrai o arquivo .zip |###
with zipfile.ZipFile(zipped, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

###| Copia os arquivos para o local correto |###
if os.path.exists(final_dir):
    shutil.rmtree(final_dir)
shutil.copytree(multi_file_folder, final_dir)

###| Deleta a pasta temp |###
try:
    shutil.rmtree(temp_dir)
except:
    pass

###| Cria o atalho |###
swl = SWinLnk()
swl.create_lnk(exe_file, shortcut_file)

win32api.MessageBox(0, "Download completo!", "Download completo")





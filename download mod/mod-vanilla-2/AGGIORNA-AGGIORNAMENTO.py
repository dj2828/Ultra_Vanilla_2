import requests
import zipfile
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

GITHUB = 'https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/main/download%20mod/down/'
COSE = ['down.py', 'leggimi.txt', 'mod per chi ha aTlauncher.py', 'mod.py', 'py.bat', 'se non worka.bat', 'AGGIORNA-AGGIORNAMENTO.py']

for i in COSE:
    os.remove(i)

response = requests.get(GITHUB + 'mod-vanilla-2.zip')
zip_path = 'temp.zip'

with open(zip_path, 'wb') as f:
    f.write(response.content)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('./')

os.remove(zip_path)
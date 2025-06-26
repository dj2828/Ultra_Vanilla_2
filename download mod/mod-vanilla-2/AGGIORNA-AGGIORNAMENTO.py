import requests
import zipfile
import os

GITHUB = 'https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/master/download%20mod/down/'
COSE = ['down.py', 'leggimi.txt', 'dom per chi ha aTlauncher.py', 'mod', 'py.bat', 'se non worka.bat', 'AGGIORNA-AGGIORNAMENTO.py']

def download_and_extract_zip(url):
    response = requests.get(url)
    zip_path = 'temp.zip'
    
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('./')
    
    os.remove(zip_path)

for i in COSE:
    os.remove(i)

download_and_extract_zip(GITHUB + 'mod-vanilla-2.zip')

os.remove('AGGIORNA-AGGIORNAMENTO.py')
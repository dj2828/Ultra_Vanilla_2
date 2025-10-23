import requests
import zipfile
import os

# Imposta la directory di lavoro alla posizione dello script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# URL base di GitHub
GITHUB = 'https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/main/releases/download/mod-vanilla-2/mod-vanilla-2.zip'
# Lista di tutti i file che compongono questo set di script
COSE = ['down.py', 'leggimi.txt', 'mod per chi ha aTlauncher.py', 'mod.py', 'py.bat', 'AGGIORNA-AGGIORNAMENTO.py']

# Rimuove tutti i file attuali per preparare l'aggiornamento
for i in COSE:
    try:
        os.remove(i)
    except FileNotFoundError:
        pass # Ignora se un file non esiste

# Scarica il file zip con la nuova versione
response = requests.get(GITHUB)
zip_path = 'temp.zip' # Nome temporaneo per il file zip

# Salva il file zip
with open(zip_path, 'wb') as f:
    f.write(response.content)

# Estrae il contenuto dello zip nella directory corrente, sovrascrivendo
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('./')

# Rimuove il file zip temporaneo
os.remove(zip_path)
import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import requests
import shutil
import time
import concurrent.futures
from tqdm import tqdm
import threading

API_KEY = "$2a$10$qP3o7IaF4x.p/GmbIBVvqOHjuZ9b.4Xc2tQ91GkW/DhVZjLIuWWpK"
HEADERS = {
    "Accept": "application/json",
    "x-api-key": API_KEY
}
MANIFEST_PATH = "manifest.json"

def ottieni_link_download(project_id, file_id):
    url = f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}/download-url"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get("data")
    else:
        tqdm.write(f"❌ Impossibile ottenere il link di download per Project ID: {project_id}, File ID: {file_id}")
        return None

def ottieni_nome_file(project_id, file_id):
    url = f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()["data"]["fileName"]
    return f"{file_id}.jar"
def ottieni_url_progetto(project_id, file_id):
    url = f"https://api.curseforge.com/v1/mods/{project_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        slug = resp.json()["data"]["slug"]  # <-- usa lo slug reale
        return f"https://www.curseforge.com/minecraft/mc-mods/{slug}/download/{file_id}"
    return file_id

def scarica_file(url, percorso_file):
    resp = requests.get(url)
    with open(percorso_file, "wb") as f:
        f.write(resp.content)

def sc(MODS_DIR):
    if not os.path.exists(MODS_DIR):
        os.makedirs(MODS_DIR)

    down_error = []
    durl = []
    lock = threading.Lock()  # Per sincronizzare tqdm e down_error

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    files = manifest.get("files", [])

    progress = tqdm(total=len(files), desc="Download mod", unit="mod")

    def scarica_mod(mod):
        project_id = mod["projectID"]
        file_id = mod["fileID"]
        nome_file = ottieni_nome_file(project_id, file_id)
        download_url = ottieni_link_download(project_id, file_id)
        if not download_url:
            with lock:
                down_error.append(nome_file)
                durl.append(ottieni_url_progetto(project_id, file_id))
            tqdm.write(f"❌ Link di download non trovato per {nome_file}")
        else:
            destinazione = os.path.join(MODS_DIR, nome_file)
            scarica_file(download_url, destinazione)
            tqdm.write(f"✅ Scaricato {nome_file}")
        with lock:
            progress.update(1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(scarica_mod, files)

    progress.close()
    return down_error, durl

def rip_sposta(MODS_DIR):
    os.makedirs('./mods/')
    lock = threading.Lock()  # Per sincronizzare tqdm

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    files = manifest.get("files", [])
    print(f"🔍 Trovate {len(files)} mod nella modlist.")
    
    if os.path.exists(MODS_DIR+'ultra_vanilla_2.jar'): shutil.move(MODS_DIR+'ultra_vanilla_2.jar', './mods/')

    progress = tqdm(total=len(files), desc="Spostamento mod", unit="mod")
    
    def sposta(mod):
        project_id = mod["projectID"]
        file_id = mod["fileID"]
        nome_file = ottieni_nome_file(project_id, file_id)

        if os.path.exists(MODS_DIR+nome_file):
            shutil.move(MODS_DIR+nome_file, './mods/')
            tqdm.write(f"⏩ Spostato {nome_file}")
        with lock:
            progress.update(1)

    for mod in files:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(sposta, mod)
        

def rip_down():
    down_error = []
    durl = []

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    files = manifest.get("files", [])

    for mod in files:
        project_id = mod["projectID"]
        file_id = mod["fileID"]

        nome_file = ottieni_nome_file(project_id, file_id)
        if os.path.exists('./mods/'+nome_file):
            continue
        
        download_url = ottieni_link_download(project_id, file_id)
        if not download_url:
            down_error.append(nome_file)
            durl.append(ottieni_url_progetto(project_id, file_id))
            print(f"❌ Link di download non trovato per {nome_file}")
            continue

        destinazione = os.path.join('./mods/', nome_file)
        scarica_file(download_url, destinazione)
        print(f"✅ Scaricato {nome_file}")
    return down_error, durl

def cancella_mod(list, MODS_DIR):
    for mod in list:
        project_id = mod["projectID"]
        file_id = mod["fileID"]
        nome_file = ottieni_nome_file(project_id, file_id)

        percorso_file = os.path.join(MODS_DIR, nome_file)
        if os.path.exists(percorso_file):
            try:
                os.remove(percorso_file)
                print(f"🗑️  Rimosso {nome_file}")
            except Exception as e:
                print(f"❌ Errore durante la rimozione di {nome_file}: {e}")
        else:
            print(f"⚠️  Il file {nome_file} non esiste nella directory.")

def aggiungi_mod(lista, MODS_DIR):
    down_error = []
    lock = threading.Lock()  # Per sincronizzare tqdm e down_error

    progress = tqdm(total=len(lista), desc="Download mod", unit="mod")

    def scarica_mod(mod):
        project_id = mod["projectID"]
        file_id = mod["fileID"]
        nome_file = ottieni_nome_file(project_id, file_id)
        download_url = ottieni_link_download(project_id, file_id)
        if not download_url or not download_url.startswith("https://"):
            with lock:
                down_error.append(nome_file)
            tqdm.write(f"❌ Link di download non trovato per {nome_file}")
        else:
            destinazione = os.path.join(MODS_DIR, nome_file)
            scarica_file(download_url, destinazione)
            tqdm.write(f"✅ Scaricato {nome_file}")
        with lock:
            progress.update(1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(scarica_mod, lista)

    progress.close()
    return down_error

def confronta_modlist(file1, file2):
    def estrai_mods(path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
            return set((mod['projectID'], mod['fileID']) for mod in data.get('files', []))

    mods1 = estrai_mods(file1)
    mods2 = estrai_mods(file2)

    cancellare = [ {'projectID': pid, 'fileID': fid} for (pid, fid) in mods1 - mods2 ]
    aggiungere = [ {'projectID': pid, 'fileID': fid} for (pid, fid) in mods2 - mods1 ]

    risultato = {
        'cancellare': cancellare,
        'aggiungere': aggiungere
    }

    with open('differenze.json', 'w', encoding='utf-8') as out:
        json.dump(risultato, out, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print("Sei down")
    input("")
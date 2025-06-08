import json
import os
import requests
import shutil
import time

API_KEY = "$2a$10$qP3o7IaF4x.p/GmbIBVvqOHjuZ9b.4Xc2tQ91GkW/DhVZjLIuWWpK"
HEADERS = {
    "Accept": "application/json",
    "x-api-key": API_KEY
}
MANIFEST_PATH = "modlist.json"

def ottieni_link_download(project_id, file_id, tentativi=3, attesa=2):
    url = f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}/download-url"
    for i in range(tentativi):
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            return resp.json().get("data")
        if i < tentativi - 1:
            print(f"⚠️  Tentativo {i+1} fallito, riprovo tra {attesa} secondi...")
            time.sleep(attesa)
    print(f"❌ Impossibile ottenere il link di download per Project ID: {project_id}, File ID: {file_id}")
    cose = str(project_id) + "-" + str(file_id)
    return cose

def ottieni_nome_file(project_id, file_id):
    url = f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()["data"]["fileName"]
    return f"{file_id}.jar"

def scarica_file(url, percorso_file):
    resp = requests.get(url)
    with open(percorso_file, "wb") as f:
        f.write(resp.content)

def sc(MODS_DIR):
    if not os.path.exists(MODS_DIR):
        os.makedirs(MODS_DIR)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    files = manifest.get("files", [])
    print(f"🔍 Trovate {len(files)} mod nella modlist.")

    for mod in files:
        project_id = mod["projectID"]
        file_id = mod["fileID"]

        download_url = ottieni_link_download(project_id, file_id)
        if not download_url:
            continue
        if not download_url.startswith("https://"):
            down_error.append(download_url)
            continue
        
        nome_file = ottieni_nome_file(project_id, file_id)
        destinazione = os.path.join(MODS_DIR, nome_file)
        scarica_file(download_url, destinazione)
        print(f"✅ Scaricato {nome_file}")
    
    return down_error if down_error else None

def upt_sposta(MODS_DIR):
    os.makedirs('./mods/')

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    files = manifest.get("files", [])
    print(f"🔍 Trovate {len(files)} mod nella modlist.")

    shutil.move(MODS_DIR+'ultra_vanilla_2.jar', './mods/')

    for mod in files:
        project_id = mod["projectID"]
        file_id = mod["fileID"]
        nome_file = ottieni_nome_file(project_id, file_id)

        if os.path.exists(MODS_DIR+nome_file):
            shutil.move(MODS_DIR+nome_file, './mods/')
            print(f"⏩ Spostato {nome_file}")
        else:
            continue

def upt_down():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    files = manifest.get("files", [])

    for mod in files:
        project_id = mod["projectID"]
        file_id = mod["fileID"]

        nome_file = ottieni_nome_file(project_id, file_id)
        if os.path.exists('./mods/'+nome_file):
            continue
        else:
            if not download_url:
            continue
            if not download_url.startswith("https://"):
                down_error.append(download_url)
                continue

            destinazione = os.path.join('./mods/', nome_file)
            scarica_file(download_url, destinazione)
            print(f"✅ Scaricato {nome_file}")
    return down_error if down_error else None

if __name__ == "__main__":
    print("Sei down")
    input("")
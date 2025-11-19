import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import requests
import shutil
import time
import concurrent.futures # Per eseguire download in parallelo (multithreading)
from tqdm import tqdm     # Per mostrare una barra di avanzamento
import threading          # Per gestire la sincronizzazione tra i thread (Lock)

# Chiave API per l'API di CurseForge
API_KEY = "$2a$10$qP3o7IaF4x.p/GmbIBVvqOHjuZ9b.4Xc2tQ91GkW/DhVZjLIuWWpK"
HEADERS = {
    "Accept": "application/json",
    "x-api-key": API_KEY
}
MANIFEST_PATH = "manifest.json" # Nome del file manifest

def GET_MANIFEST():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    files = manifest.get("files", [])
    return files

# Ottiene il link di download per un file specifico dall'API di CurseForge
def ottieni_link_download(project_id, file_id):
    url = f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}/download-url"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json().get("data") # Ritorna l'URL di download
    else:
        # Scrive sulla console (tqdm.write) senza rovinare la barra di avanzamento
        tqdm.write(f"❌ Impossibile ottenere il link di download per Project ID: {project_id}, File ID: {file_id}")
        return None

# Ottiene il nome del file (es. "jei-1.20.1.jar") dall'API di CurseForge
def ottieni_nome_file(project_id, file_id):
    url = f"https://api.curseforge.com/v1/mods/{project_id}/files/{file_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()["data"]["fileName"]
    return f"{file_id}.jar" # Fallback se l'API fallisce

# Ottiene l'URL della pagina web del progetto (per il download manuale)
def ottieni_url_progetto(project_id, file_id):
    url = f"https://api.curseforge.com/v1/mods/{project_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        slug = resp.json()["data"]["slug"]  # Ottiene lo "slug" (es. "just-enough-items-jei")
        # Costruisce l'URL della pagina di download
        return f"https://www.curseforge.com/minecraft/mc-mods/{slug}/download/{file_id}"
    return file_id # Fallback

# Funzione helper per scaricare un file da un URL
def scarica_file(url, percorso_file):
    resp = requests.get(url)
    with open(percorso_file, "wb") as f:
        f.write(resp.content)

# Funzione principale per scaricare le mod (usata da 'scarica_mod' e 'rip_mod')
def sc(MODS_DIR, gia_messe=False):
    if not os.path.exists(MODS_DIR):
        os.makedirs(MODS_DIR)

    down_error = [] # Lista dei file falliti
    durl = []       # Lista degli URL per il download manuale
    lock = threading.Lock()  # Lock per l'accesso sicuro a 'down_error', 'durl' e 'tqdm'

    if gia_messe:
        # Se 'gia_messe' è fornito (dalla funzione rip_mod), 
        # 'files' diventa la lista delle mod MANCANTI.
        files = gia_messe
    else:
        # Altrimenti (installazione normale), carica il manifest standard
        files = GET_MANIFEST()

    # Inizializza la barra di avanzamento
    progress = tqdm(total=len(files), desc="Download mod", unit="mod")

    # Funzione eseguita da ogni thread per scaricare una singola mod
    def scarica_mod(mod):
        project_id = mod["projectID"]
        file_id = mod["fileID"]
        nome_file = ottieni_nome_file(project_id, file_id)
        download_url = ottieni_link_download(project_id, file_id)
        
        if not download_url or not download_url.startswith("https://"): # Se l'API non fornisce un URL
            with lock: # Usa il lock per aggiornare le liste in modo sicuro
                down_error.append(nome_file)
                durl.append(ottieni_url_progetto(project_id, file_id))
            tqdm.write(f"❌ Link di download non trovato per {nome_file}")
        else:
            # Scarica il file
            destinazione = os.path.join(MODS_DIR, nome_file)
            scarica_file(download_url, destinazione)
            tqdm.write(f"✅ Scaricato {nome_file}")
        
        with lock: # Usa il lock per aggiornare la barra di avanzamento
            progress.update(1)

    # Avvia i download in parallelo usando un ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scarica_mod, files) # 'map' applica 'scarica_mod' a ogni elemento in 'files'

    progress.close() # Chiude la barra di avanzamento
    return down_error, durl # Ritorna le liste di errori

# Funzione per "riparare": sposta le mod valide dalla cartella corrotta
def rip_sposta(MODS_DIR, server=False):
    mods = os.path.join(os.getcwd(), "mod") if server else os.path.join(os.getcwd(), "mods")
    os.makedirs(mods, exist_ok=True) # Crea la cartella temporanea
    lock = threading.Lock()

    files = GET_MANIFEST() # Lista di *tutte* le mod del manifest
    print(f"🔍 Trovate {len(files)} mod nella modlist.")
    
    # Sposta il JAR personalizzato se esiste
    if os.path.exists(MODS_DIR+'ultra_vanilla_2.jar'): shutil.move(MODS_DIR+'ultra_vanilla_2.jar', mods)
    if os.path.exists(MODS_DIR+'noisium-forge-2.3.0+mc1.20-1.20.1.jar'): shutil.move(MODS_DIR+'noisium-forge-2.3.0+mc1.20-1.20.1.jar', mods)

    progress = tqdm(total=len(files), desc="Spostamento mod", unit="mod")
    
    gia_messe = [] # Lista delle mod trovate e spostate
    
    # Funzione eseguita dai thread
    def sposta(mod):
        project_id = mod["projectID"]
        file_id = mod["fileID"]
        # Ottiene il nome file *corretto* dall'API
        nome_file = ottieni_nome_file(project_id, file_id)

        # Controlla se il file esiste nella cartella mods
        if os.path.exists(MODS_DIR+nome_file):
            shutil.move(MODS_DIR+nome_file, mods) # Sposta nella cartella temporanea
            with lock:
                gia_messe.append(mod) # Aggiunge alla lista delle mod salvate
            tqdm.write(f"⏩ Spostato {nome_file}")
        
        with lock:
            progress.update(1) # Aggiorna la barra sia che il file sia stato trovato o meno

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(sposta, files)

    progress.close()

    # Crea una nuova lista 'mancanti' contenente solo le mod in 'files'
    # che non sono state aggiunte a 'gia_messe' (correzione dalla scorsa volta)
    mancanti = [mod for mod in files if mod not in gia_messe]

    # Ritorna la lista delle mod MANCANTI
    return mancanti if mancanti != [] else False
        
# --- Funzione Commentata ---
# Questa funzione è chiamata da mod.py (in una versione precedente) ma è commentata qui.
# Probabilmente serviva a scaricare i file *mancanti* dopo rip_sposta,
# ma ora la logica è stata integrata in rip_sposta (che ritorna le mod mancanti)
# e in rip_mod (che le passa a 'sc').
#
# def rip_down():
#     down_error = []
#     durl = []
# 
#     with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
#         manifest = json.load(f)
# 
#     files = manifest.get("files", [])
# 
#     for mod in files:
#         project_id = mod["projectID"]
#         file_id = mod["fileID"]
# 
#         nome_file = ottieni_nome_file(project_id, file_id)
#         # Controlla se è già stato spostato
#         if os.path.exists('./mods/'+nome_file):
#             continue
#         
#         download_url = ottieni_link_download(project_id, file_id)
#         if not download_url:
#             down_error.append(nome_file)
#             durl.append(ottieni_url_progetto(project_id, file_id))
#             print(f"❌ Link di download non trovato per {nome_file}")
#             continue
# 
#         destinazione = os.path.join('./mods/', nome_file)
#         scarica_file(download_url, destinazione)
#         print(f"✅ Scaricato {nome_file}")
#     return down_error, durl
# ------------------------------

# Funzione per cancellare una lista di mod
def cancella_mod(list, MODS_DIR):
    for mod in list:
        project_id = mod["projectID"]
        file_id = mod["fileID"]
        nome_file = ottieni_nome_file(project_id, file_id) # Ottiene il nome file da rimuovere

        percorso_file = os.path.join(MODS_DIR, nome_file)
        if os.path.exists(percorso_file):
            try:
                os.remove(percorso_file) # Rimuove il file
                print(f"🗑️  Rimosso {nome_file}")
            except Exception as e:
                print(f"❌ Errore durante la rimozione di {nome_file}: {e}")
        else:
            print(f"⚠️  Il file {nome_file} non esiste nella directory.")

# Funzione per aggiungere una lista di mod (usata da 'upt_mod')
def aggiungi_mod(lista, MODS_DIR):
    down_error = []
    durl = []
    lock = threading.Lock()

    progress = tqdm(total=len(lista), desc="Download mod", unit="mod")

    # Funzione per il thread (simile a 'scarica_mod' in 'sc')
    def scarica_mod(mod):
        project_id = mod["projectID"]
        file_id = mod["fileID"]
        nome_file = ottieni_nome_file(project_id, file_id)
        download_url = ottieni_link_download(project_id, file_id)
        
        if not download_url or not download_url.startswith("https://"): # Se l'API non fornisce un URL
            with lock: # Usa il lock per aggiornare le liste in modo sicuro
                down_error.append(nome_file)
                durl.append(ottieni_url_progetto(project_id, file_id))
            tqdm.write(f"❌ Link di download non trovato per {nome_file}")
        else:
            # Scarica il file
            destinazione = os.path.join(MODS_DIR, nome_file)
            scarica_file(download_url, destinazione)
            tqdm.write(f"✅ Scaricato {nome_file}")
        
        with lock:
            progress.update(1)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scarica_mod, lista)

    progress.close()
    return down_error, durl # Ritorna solo la lista dei nomi dei file falliti

# Funzione per confrontare due file manifest
def confronta_modlist(file1, file2):
    # Funzione helper per estrarre gli ID delle mod da un manifest
    def estrai_mods(path):
        try:
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
                # Crea un 'set' (insieme) di tuple (projectID, fileID)
                # I set sono efficienti per trovare le differenze
                return set((mod['projectID'], mod['fileID']) for mod in data.get('files', []))
        except FileNotFoundError:
            print(f"Errore: File manifest non trovato a {path}")
            return set() # Ritorna un set vuoto se il file non esiste
        except json.JSONDecodeError:
            print(f"Errore: File manifest corrotto a {path}")
            return set() # Ritorna un set vuoto se il JSON non è valido

    mods1 = estrai_mods(file1) # Mod installate (vecchio manifest)
    mods2 = estrai_mods(file2) # Mod da installare (nuovo manifest)

    # Calcola le differenze usando la sottrazione tra set
    # mods1 - mods2 = mod che sono in 1 ma non in 2 (da cancellare)
    cancellare = [ {'projectID': pid, 'fileID': fid} for (pid, fid) in mods1 - mods2 ]
    # mods2 - mods1 = mod che sono in 2 ma non in 1 (da aggiungere)
    aggiungere = [ {'projectID': pid, 'fileID': fid} for (pid, fid) in mods2 - mods1 ]

    risultato = {
        'cancellare': cancellare,
        'aggiungere': aggiungere
    }

    # Scrive le differenze in un file JSON
    with open('differenze.json', 'w', encoding='utf-8') as out:
        json.dump(risultato, out, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # Se lo script viene eseguito direttamente
    print("Sei down")
    input("")
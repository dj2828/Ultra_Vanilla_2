import os
import shutil  # Per operazioni su file e cartelle (spostare, rimuovere)
import sys     # Per uscire dallo script (sys.exit)
import requests # Per scaricare file da Internet (manifest, mod, zip)
import zipfile  # Per estrarre file .zip
import down     # Il tuo modulo personalizzato (down.py) per gestire i download delle mod
import filecmp  # Per confrontare file (usato per vedere se il manifest è cambiato)
import json     # Per leggere file JSON (il manifest e differenze.json)
import webbrowser # Per aprire il browser web (per i download manuali)

# Imposta la directory di lavoro corrente alla posizione dello script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Variabili Globali ---
USER = os.getlogin()  # Ottiene il nome utente di Windows
mod = False  # Flag per sapere se è stata eseguita un'operazione sulle mod (per la pulizia finale)
# URL base su GitHub da cui scaricare i file (manifest, zip, ecc.)
GITHUB = 'https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/main/download%20mod/down/'

try:
    # Funzione chiamata alla fine dello script per pulire e uscire
    def fine():
        os.system('cls')  # Pulisce la console
        try:
            shutil.rmtree('__pycache__/')  # Rimuove la cache di Python
        except:
            pass
        
        if mod:  # Se è stata fatta un'operazione sulle mod
            try:
                # Rimuove il vecchio manifest dall'istanza e il file delle differenze
                os.remove(MINECRAFT+'mods/manifest.json')
                os.remove('differenze.json')
                if crack:
                    os.remove('forge.jar')
                    os.remove('forge.jar.log')
            except:
                pass  # Ignora errori se i file non esistono
            # Sposta il nuovo manifest.json scaricato nella cartella mods
            shutil.move('manifest.json', MINECRAFT+'mods/manifest.json')

        print('\n\033[92mOra prova ad aprire ATlaunche COME OFFLINE\033[0m' if not crack else '\n\033[92mOra prova ad aprire minecarft 1.20.1 forge 47.4.0\033[0m')
        input('')  # Attende l'input dell'utente prima di chiudere
        sys.exit() # Esce dallo script

    # Funzione per scaricare e installare il texture pack
    def tx():
        print('\n\033[92mScaricamento texturepack\nAttendi...\033[0m')
        # Scarica il file zip del texture pack da GitHub
        response = requests.get(GITHUB+'Ultra-vanilla-2.zip')
        with open('Ultra-vanilla-2.zip', 'wb') as f:
            f.write(response.content)
        
        # Rimuove il vecchio texture pack se esiste
        if os.path.exists(MINECRAFT+'resourcepacks/Ultra-vanilla-2.zip'):
            os.remove(MINECRAFT+'resourcepacks/Ultra-vanilla-2.zip')
        # Crea la cartella resourcepacks se non esiste
        if not os.path.exists(MINECRAFT+'resourcepacks/'):
            os.makedirs(MINECRAFT+'resourcepacks/')
            
        # Sposta il nuovo texture pack nella cartella resourcepacks
        shutil.move('Ultra-vanilla-2.zip', MINECRAFT+'resourcepacks/')
        
        print('Texture pack installata')
        input('\033[92mPremere invio\033[0m ')
        
        fine() # Chiama la funzione di fine

    # Funzione per scaricare e installare "cose" (file di configurazione, ecc.)
    # 'a' è un booleano: True = aggiornamento (rimuove i vecchi file), False = installazione (non rimuove)
    def cose(a):
        # Scarica cose.zip
        response = requests.get(GITHUB+'cose.zip')
        with open('cose.zip', 'wb') as f:
            f.write(response.content)
        print('\nScaricato cose.zip')

        # Estrae cose.zip in una cartella temporanea 'cosse'
        with zipfile.ZipFile('cose.zip', 'r') as zip_ref:
            os.makedirs('cosse/')
            zip_ref.extractall('cosse/')
        print('Cose estratte')

        # Legge il file 'cose.txt' che contiene le istruzioni
        with open('./cosse/cose.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Salta linee vuote

                dirr = False  # Flag per sapere se è una directory
                operation = line[0]  # Legge l'operazione (+ = aggiungi/sostituisci, altro = ?)
                name, _ = line.split(';')
                if '.' not in name:
                    dirr = True  # Se non c'è un punto, assume sia una directory
                
                if operation != '+':
                    # Logica per operazioni diverse da '+'
                    if a:  # Se è un aggiornamento (a=True), salta questa operazione
                        continue
                    else: # Se è un'installazione (a=False)
                        name, dire = line.split(';')
                        dire = MINECRAFT+dire # Costruisce il percorso di destinazione
                        if dirr:
                            shutil.move('cosse/'+name, dire) # Sposta la directory
                        else:
                            if os.path.exists(dire)==False:
                                os.makedirs(dire) # Crea la cartella se non esiste
                            shutil.move('cosse/'+name, dire+name) # Sposta il file
                        print('Spostato '+name)
                else:
                    # Logica per operazione '+' (aggiungi/sostituisci)
                    rest = line[1:]
                    name, dire = rest.split(';')
                    dire = MINECRAFT+dire
                    if a or crack: # Se è un aggiornamento (a=True), prova a rimuovere il vecchio file/dir
                        try:
                            if dirr:
                                shutil.rmtree(dire)
                            else:
                                os.remove(dire+name)
                        except:
                            pass # Ignora errori se il file non esiste
                    # Sposta il nuovo file/dir
                    if dirr:
                        shutil.move('cosse/'+name, dire)
                    else:
                        if os.path.exists(dire)==False:
                            os.makedirs(dire)
                        shutil.move('cosse/'+name, dire+name)
                    print('Spostato '+name)
        
        # Pulizia dei file temporanei
        os.remove('cose.zip')
        shutil.rmtree('cosse/')
        if mod: # Se era un'operazione mod, aggiorna anche il texture pack
            tx()
        else: # Altrimenti, finisci
            fine()

    def scarica_mod():
        print("\n\033[92mOra si scaricheranno le mod. premere INVIO")
        input('')
        print("Attendi...\033[0m\n")

        if crack:
            # Scarica l'installer di Forge
            with open('forge.jar', 'wb') as f:
                response = requests.get('https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.4.0/forge-1.20.1-47.4.0-installer.jar')
                f.write(response.content)
            print('Scaricato forge.jar')

        # Chiama la funzione 'sc' dal modulo 'down' per scaricare le mod dal manifest
        down_error, durl = down.sc(MINECRAFT+'mods/')
        # Scarica il file JAR personalizzato
        down.scarica_file(GITHUB+'ultra_vanilla_2.jar', MINECRAFT+'mods/ultra_vanilla_2.jar')

        if down_error: # Se ci sono stati errori di download
            os.system("cls")
            print("\033[91mATTENZIONE: alcune mod non sono state scaricate\033[0m")
            print("Le mod che non sono state scaricate sono:")
            for error in down_error:
                print(error)
            # Apre il browser per il download manuale
            input('\n\033[91mPremere invio per scaricarle dal browser (SE DELLE MOD DA ERRORE 404, CERCATELE E SCARICATELE TE)\033[0m')
            for i in range(len(durl)):
                print(f"{down_error[i]}: {durl[i]}\n")
                webbrowser.open(durl[i]) # Apre il link di download nel browser
            input('\n\033[91mPremere invio una volta finite di scaricare\033[0m')
            # Tenta di spostare le mod scaricate manually dalla cartella Downloads
            for i in down_error:
                try:
                    # Sposta il file dalla cartella Downloads dell'utente alla cartella mods
                    shutil.move(f"C:\\Users\\{USER}\\Downloads\\{i}", MINECRAFT+'mods/')
                except Exception as e:
                    print(f"Errore nello spostare {i}: {e}") # Stampa un errore se lo spostamento fallisce

        if crack:
            print("\033[92mPremere INVIO\033[0m")
            input('')
            # Avvia l'installer di Forge
            print('\033[92mOra comparirà una finestra per installare forge, tu prosegui')
            input('Premi INVIO per iniziare\033[0m ')
            os.system('start '+'./forge.jar') # Esegue il file .jar
            print('\n\033[92mUna volta finito premi INVIO\033[0m')
            input('') # Attende che l'utente finisca l'installazione manuale

        print('Mod scaricate')
        cose(False) # Chiama 'cose' in modalità installazione (False)

    # Funzione per aggiornare le mod
    def upt_mod():
        print("\n\033[92mOra si aggiorneranno le mod. premere INVIO")
        input('')
        print("Attendi...\033[0m\n")

        # Confronta il manifest locale con quello nuovo e scrive le differenze in 'differenze.json'
        down.confronta_modlist(MINECRAFT+'mods/manifest.json', 'manifest.json')

        # Legge 'differenze.json'
        with open('differenze.json', "r", encoding="utf-8") as f:
            manifest = json.load(f)
            cancellare = manifest.get("cancellare", []) # Lista mod da cancellare
            aggiungere = manifest.get("aggiungere", []) # Lista mod da aggiungere

        if cancellare:
            down.cancella_mod(cancellare, MINECRAFT+'mods/') # Cancella le mod vecchie
        
        # Sposta temporaneamente 'mcef-libraries' (probabilmente per evitare che venga cancellato)
        if os.path.exists(MINECRAFT+'mods/mcef-libraries/'): shutil.move(MINECRAFT+'mods/mcef-libraries/', './mcef-libraries/')
        # Rimuove il vecchio JAR personalizzato
        if os.path.exists(MINECRAFT+'mods/ultra_vanilla_2.jar'): os.remove(MINECRAFT+'mods/ultra_vanilla_2.jar')

        # Scarica le mod nuove
        down_error = [] # Inizializza la lista di errori
        durl = []
        if aggiungere:
            down_error, durl = down.aggiungi_mod(aggiungere, MINECRAFT+'mods/')
        
        # Rimette a posto 'mcef-libraries'
        if os.path.exists('./mcef-libraries/'): shutil.move('./mcef-libraries/', MINECRAFT+'mods/mcef-libraries/')
        # Scarica il nuovo JAR personalizzato
        down.scarica_file(GITHUB+'ultra_vanilla_2.jar', MINECRAFT+'mods/ultra_vanilla_2.jar')

        if down_error: # Se ci sono stati errori di download
            print("\033[91mATTENZIONE: alcune mod non sono state scaricate\033[0m")
            print("Le mod che non sono state scaricate sono:")
            for error in down_error:
                print(error)
            # Apre il browser per il download manuale
            input('\n\033[91mPremere invio per scaricarle dal browser (SE DELLE MOD DA ERRORE 404, CERCATELE E SCARICATELE TE)\033[0m')
            for i in range(len(durl)):
                print(f"{down_error[i]}: {durl[i]}\n")
                webbrowser.open(durl[i]) # Apre il link di download nel browser
            input('\n\033[91mPremere invio una volta finite di scaricare\033[0m')
            # Tenta di spostare le mod scaricate manually dalla cartella Downloads
            for i in down_error:
                try:
                    # Sposta il file dalla cartella Downloads dell'utente alla cartella mods
                    shutil.move(f"C:\\Users\\{USER}\\Downloads\\{i}", MINECRAFT+'mods/')
                except Exception as e:
                    print(f"Errore nello spostare {i}: {e}") # Stampa un errore se lo spostamento fallisce

        print('Mod aggiornate')

        # Chiede se aggiornare anche 'cose'
        cos = input('\n\033[92mVuoi anche aggiornare cose? (s/n) \033[0m')
        if cos == 's':
            cose(True) # Chiama 'cose' in modalità aggiornamento
        elif cos == 'n':
            tx() # Altrimenti aggiorna solo il texture pack

    # Funzione per riparare le mod
    def rip_mod(full):
        print("\n\033[92mOra si ripareranno le mod. premere INVIO")
        input('')
        print("Attendi...\033[0m\n")
        
        # Sposta le mod valide esistenti in una cartella temporanea './mods'
        if not full:
            da_mettere = down.rip_sposta(MINECRAFT+'mods/')
        else:
            da_mettere = down.GET_MANIFEST()

        # Rimuove la vecchia cartella mods (corrotta)
        shutil.rmtree(MINECRAFT+'mods/')
        
        # Scarica il JAR personalizzato se non è stato salvato
        if not os.path.exists('./mods/ultra_vanilla_2.jar'): down.scarica_file(GITHUB+'ultra_vanilla_2.jar', './mods/ultra_vanilla_2.jar')
        
        # Chiama 'sc' passando la lista delle mod MANCANTI ('da_mettere')
        down_error, durl = down.sc(MINECRAFT+'mods/', da_mettere)

        # Sposta le mod salvate (da './mods') nella nuova cartella mods
        shutil.move('./mods/', MINECRAFT+'mods/')

        if down_error: # Se ci sono stati errori di download
            print("\033[91mATTENZIONE: alcune mod non sono state scaricate\033[0m")
            print("Le mod che non sono state scaricate sono:")
            for error in down_error:
                print(error)
            # Apre il browser per il download manuale
            input('\n\033[91mPremere invio per scaricarle dal browser (SE DELLE MOD DA ERRORE 404, CERCATELE E SCARICATELE TE)\033[0m')
            for i in range(len(durl)):
                print(f"{down_error[i]}: {durl[i]}\n")
                webbrowser.open(durl[i])
            input('\n\033[91mPremere invio una volta finite di scaricare\033[0m')
            # Tenta di spostare le mod scaricate manualmente dalla cartella Downloads
            for i in down_error:
                try:
                    shutil.move(f"C:\\Users\\{USER}\\Downloads\\{i}", MINECRAFT+'mods/')
                except Exception as e:
                    print(f"Errore nello spostare {i}: {e}")

        print('Mod riparate')
        tx() # Aggiorna il texture pack

# --- Inizio Esecuzione Script ---
    print(USER)
    print("Benvenuto nell' installer delle mod")
    print('SEI DA COSA?')
    print('1: ATlauncher\n2: Launcher normale | Tlauncher')
    cos = input('')
    crack = False if cos == '1' else True # Flag per sapere se NON è ATlauncher
    # Percorso dell'istanza di Minecraft
    MINECRAFT = os.path.join(os.getenv('APPDATA'), 'ATLauncher/instances/Ultravanilla2/' if not crack else '.minecraft/')

    print("\nSe devi scaricare le mod scrivi 's'\nSe devi aggiornare scrivi 'a'\nSe devi riparare le mod scrivi 'r'\nSe devi aggiornare la texture pack scrivi 'tx'\nSe devi aggiornare altre cose scrivi 'cose'")
    cos = input('') # Legge la scelta dell'utente
    os.system('cls') # Pulisce lo schermo
    
    if cos == 's': # SCARICA
        response = requests.get(GITHUB+'manifest.json') # Scarica il manifest
        with open('manifest.json', 'wb') as f:
            f.write(response.content)
        print(f'Scaricato manifest.json')

        # --- DIFFERENZA crack ---
        # Controllo di sicurezza: costringe l'utente a rimuovere la cartella mods
        # esistente prima di procedere con una nuova installazione.
        if crack:
            while os.path.exists(MINECRAFT+'mods'):
                print('\033[91mLa cartella mods esiste ancora, rinominala o cancellala. premi INVIO\033[0m')
                input('')
                os.system('start '+MINECRAFT) # Apre la cartella .minecraft
                print('Una volta fatto premi INVIO')
                input('')
            os.makedirs(MINECRAFT+'mods/') # Crea la nuova cartella mods
        # ------------------

        mod = True # Imposta il flag mod
        scarica_mod()

    elif cos == 'a': # AGGIORNA
        # Controllo di sicurezza: verifica che esista un manifest da aggiornare
        if not os.path.exists(MINECRAFT+'mods/' and not crack): # Controlla se la cartella mods esiste
            print("\033[91mLa cartella mods non esiste, quindi scegli 'scaricare'. premi INVIO\033[0m")
            input('')
            sys.exit()
        elif not os.path.exists(MINECRAFT+'mods/manifest.json' and crack):
            print("\033[91mLa cartella mods non esiste o è stata rinominata, quindi scegli 'scaricare', rinominala in 'mods' o riparare. premi INVIO\033[0m")
            input('')
            os.system('start '+MINECRAFT)
            sys.exit()
        
        response = requests.get(GITHUB+'manifest.json') # Scarica nuovo manifest
        with open('manifest.json', 'wb') as f:
            f.write(response.content)
        print(f'Scaricato manifest.json')
        mod = True # Imposta il flag mod
        
        # Confronta il nuovo manifest con quello vecchio
        if filecmp.cmp("manifest.json", MINECRAFT+'mods/manifest.json', shallow=False):
            print("\033[92mLe mod sono già aggiornate\033[0m")
            cos = input('\n\033[92mVuoi anche aggiornare cose? (s/n) \033[0m')
            if cos == 's':
                cose(True)
            elif cos == 'n':
                tx()
        else: # Se i manifest sono diversi, aggiorna
            upt_mod()

    elif cos == 'r': # RIPARA
        cos = input('\n\033[92mVuoi reinstallare tutte le mod o solo scaricare quelle che non ci sono (1/2) \033[0m')
        if cos=="1":
            full = True
        response = requests.get(GITHUB+'manifest.json')
        with open('manifest.json', 'wb') as f:
            f.write(response.content)
        print(f'Scaricato manifest.json')
        mod = True
        rip_mod(full)

    elif cos == 'tx': # TEXTURE PACK
        tx()

    elif cos == 'cose': # COSE
        cose(True) # Chiama 'cose' in modalità aggiornamento

except SystemExit:
    raise # Permette a sys.exit() di funzionare correttamente
except Exception as e:
    # Gestione generica degli errori
    os.system('cls')
    print("\033[91mERRORE\033[0m")
    print('\033[91mChiedi a dj\033[0m')
    input(e) # Mostra l'errore e attende l'input
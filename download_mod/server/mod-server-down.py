import os
import requests
os.chdir(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists('./down.py'):
    with open('down.py', 'wb') as f_out:
        response = requests.get('https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/main/download_mod/mod-vanilla-2/down.py')
        f_out.write(response.content)
import shutil
import sys
import zipfile
import down
import filecmp
import json
import webbrowser

USER = os.getlogin()
MINECRAFT = './'
GITHUB = 'https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/main/download_mod/down/'
mod = False
OS = False if os.name == 'nt' else True

try:
    def fine():
        os.system('cls')  # Pulisce la console
        try:
            shutil.rmtree('__pycache__/')  # Rimuove la cache di Python
        except:
            pass
        
        if mod:  # Se è stata fatta un'operazione sulle mod
            os.remove('down.py')
            try:
                # Rimuove il vecchio manifest dall'istanza e il file delle differenze
                os.remove(MINECRAFT+'mods/manifest.json')
                os.remove('differenze.json')
            except:
                pass  # Ignora errori se i file non esistono
            # Sposta il nuovo manifest.json scaricato nella cartella mods
            shutil.move('manifest.json', MINECRAFT+'mods/manifest.json')

        print('\n\033[92mFatto\033[0m')
        input('')
        sys.exit()

    def cose(a):
        # Scarica cose-server.zip
        response = requests.get(GITHUB+'cose-server.zip')
        with open('cose-server.zip', 'wb') as f:
            f.write(response.content)
        print('\nScaricato cose-server.zip')

        # Estrae cose-server.zip in una cartella temporanea 'cosse'
        with zipfile.ZipFile('cose-server.zip', 'r') as zip_ref:
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
                    if a: # Se è un aggiornamento (a=True), prova a rimuovere il vecchio file/dir
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
        os.remove('cose-server.zip')
        shutil.rmtree('cosse/')
        fine()

    def fix_mod(a=False):
        response = requests.get('https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/main/download_mod/down/modlist-server.txt')
        with open('modlist-server.txt', 'wb') as f_out:
            f_out.write(response.content)
            print('Scaricato modlist-server.txt')

        with open('modlist-server.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                if line[0] == '-':
                    line = line[1:]
                    line+='.jar'
                    if os.path.exists('./mods/'+line):
                        os.remove('./mods/'+line)
                        print(f'Cancellato {line}')
                else:
                    nome, modlink = line.split(';')
                    if not os.path.exists('./mods/' + nome + '.jar'):
                        response = requests.get(modlink)
                        with open('./mods/' + nome + '.jar', 'wb') as f:
                            f.write(response.content)
                        print(f'Scaricato {nome}')
        os.remove('modlist-server.txt')
        cose(a)

    def scarica_mod():
        with open('forge.jar', 'wb') as f:
            response = requests.get('https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.4.0/forge-1.20.1-47.4.0-installer.jar')
            f.write(response.content)
        print('Scaricato forge.jar')
        if OS:
            with open('controllo.sh', 'wb') as f:
                response = requests.get('https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/main/download_mod/server/controllo.sh')
                f.write(response.content)
            print('Scaricato controllo.sh')

        # installa_forge

        print('\033[92mOra comparirà una finestra per installare forge, tu prosegui')
        input('Premi INVIO per iniziare\033[0m ')
        if OS:
            os.system("java -jar forge.jar --installServer")
            os.system("clear")
        else:
            os.system('start '+'./forge.jar')
            print('\n\033[92mUna volta finito premi INVIO\033[0m')
            input('')

        try:
            os.remove('forge.jar')
            os.remove('forge.jar.log')
        except:
            pass

        print("\n\033[92mOra si scaricheranno le mod.")
        print("Attendi...\033[0m\n")
        
        down_error, durl = down.sc(MINECRAFT+'mods/')
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
        print('Mod scaricate')

        fix_mod()

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
        
        # Rimuove il vecchio JAR personalizzato
        if os.path.exists(MINECRAFT+'mods/ultra_vanilla_2.jar'): os.remove(MINECRAFT+'mods/ultra_vanilla_2.jar')

        # Scarica le mod nuove
        if aggiungere:
            down_error = [] # Inizializza la lista di errori
            durl = []
            down_error, durl = down.aggiungi_mod(aggiungere, MINECRAFT+'mods/')
        
        # Scarica il nuovo JAR personalizzato
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

        print('Mod aggiornate')

        fix_mod(True)

    def rip_mod(full):
        print("\n\033[92mOra si ripareranno le mod. premere INVIO")
        input('')
        print("Attendi...\033[0m\n")
        
        # Sposta le mod valide esistenti in una cartella temporanea './mods'
        if not full:
            da_mettere = down.rip_sposta(MINECRAFT+'mods/', server=True)
        else:
            da_mettere = down.GET_MANIFEST()

        # Rimuove la vecchia cartella mods (corrotta)
        shutil.rmtree(MINECRAFT+'mods/')
        
        # Scarica il JAR personalizzato se non è stato salvato
        if not os.path.exists('./mod/ultra_vanilla_2.jar'): down.scarica_file(GITHUB+'ultra_vanilla_2.jar', './mod/ultra_vanilla_2.jar')
        
        if da_mettere:
            # Chiama 'sc' passando la lista delle mod MANCANTI ('da_mettere')
            down_error, durl = down.sc('./mod/', da_mettere)

            # Sposta le mod salvate (da './mod') nella nuova cartella mods
            shutil.move('./mod/', MINECRAFT+'mods/')

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
                    webbrowser.open(durl[i])
                input('\n\033[91mPremere invio una volta finite di scaricare\033[0m')
                # Tenta di spostare le mod scaricate manualmente dalla cartella Downloads
                for i in down_error:
                    try:
                        shutil.move(f"C:\\Users\\{USER}\\Downloads\\{i}", MINECRAFT+'mods/')
                    except Exception as e:
                        print(f"Errore nello spostare {i}: {e}")
        else:
            # Sposta le mod salvate (da './mod') nella nuova cartella mods
            shutil.move('./mod/', MINECRAFT+'mods/')

        print('Mod riparate')

        fix_mod()

    print(USER)
    print("Benvenuto nell' installer delle mod")
    print("Se devi scaricare le mod scrivi 's'\nSe devi aggiornare scrivi 'a'\nSe devi riparare le mod scrivi 'r'")
    cos = input('')
    os.system('cls')
    if cos == 's':
        response = requests.get(GITHUB+'manifest.json')
        with open('manifest.json', 'wb') as f:
            f.write(response.content)
        print(f'Scaricato manifest.json')

        os.makedirs(MINECRAFT+'mods/')

        mod = True
        scarica_mod()

    elif cos == 'a':
        if not os.path.exists(MINECRAFT+'mods/manifest.json'):
            print("\033[91mLa cartella mods non esiste o è stata rinominata, quindi scegli 'scaricare'. premi INVIO\033[0m")
            input('')
            sys.exit()
        response = requests.get(GITHUB+'manifest.json')
        with open('manifest.json', 'wb') as f:
            f.write(response.content)
        print(f'Scaricato manifest.json')
        mod = True
        if filecmp.cmp("manifest.json", MINECRAFT+'mods/manifest.json', shallow=False):
            print("\033[92mLe mod sono già aggiornate\033[0m")
            cos = input('\n\033[92mVuoi anche aggiornare cose? (s/n) \033[0m')
            if cos == 's':
                cose(True)
            elif cos == 'n':
                fine()
        upt_mod()

    elif cos == 'r': # RIPARA
        full = False
        cos = input('\n\033[92mVuoi reinstallare tutte le mod o solo scaricare quelle che non ci sono (1/2) \033[0m')
        if cos=="1":
            full = True
        response = requests.get(GITHUB+'manifest.json')
        with open('manifest.json', 'wb') as f:
            f.write(response.content)
        print(f'Scaricato manifest.json')
        mod = True
        rip_mod(full)
except SystemExit:
    raise
except Exception as e:
    os.system('cls')
    print("\033[91mERRORE\033[0m")
    print('\033[91mAPRI "se non worka.bat". se non va neanche quello chiedi a dj \033[0m')
    input(e)
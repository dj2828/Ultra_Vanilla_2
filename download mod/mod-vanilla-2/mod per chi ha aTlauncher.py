import os
import shutil
import sys
import requests
import zipfile
import down
import filecmp
import json
import webbrowser

global USER
USER = os.getlogin()
global agg, sc
MINECRAFT = 'C:/users/'+USER+'/AppData/Roaming/ATLauncher/instances/Ultravanilla2/'
GITHUB = 'https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/master/download%20mod/down/'
agg=False
sc=False

# try:
def fine():
    os.system('cls')
    if agg:
        shutil.rmtree('__pycache__/')
        try:
            os.remove(MINECRAFT+'mods/modlist.json')
        except:
            pass
        shutil.move('modlist.json', MINECRAFT+'mods/modlist.json')

        print('\n\033[92mOra prova ad aprire ATlaunche COME OFFLINE\033[0m')
        input('')
    elif sc:
        shutil.rmtree('__pycache__/')
        shutil.move('modlist.json', MINECRAFT+'mods/modlist.json')
        print('\n\033[92mOra prova ad aprire ATlaunche COME OFFLINE\033[0m')
        input('')
    sys.exit()

def tx():
    print('\033[92mScaricamento texturepack\nAttendi...\033[0m')
    response = requests.get(GITHUB+'Ultra-vanilla-2.zip')
    with open('Ultra-vanilla-2.zip', 'wb') as f:
        f.write(response.content)
    
    if os.path.exists(MINECRAFT+'resourcepacks/Ultra-vanilla-2.zip'):
        os.remove(MINECRAFT+'resourcepacks/Ultra-vanilla-2.zip')
    if os.path.exists(MINECRAFT+'resourcepacks/') == False:
        os.makedirs(MINECRAFT+'resourcepacks/')
        
    shutil.move('Ultra-vanilla-2.zip', MINECRAFT+'resourcepacks/')
    
    print('Texture pack installata')
    input('\033[92mPremere invio\033[0m ')
    
    fine()

def cose(a):
# scarica cose
    response = requests.get(GITHUB+'cose.zip')
    with open('cose.zip', 'wb') as f:
        f.write(response.content)
    print('\nScaricato cose.zip')

    with zipfile.ZipFile('cose.zip', 'r') as zip_ref:
        os.makedirs('cosse/')
        zip_ref.extractall('cosse/')
    print('Cose estratte')

    with open('./cosse/cose.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            dirr = False

            operation = line[0]
            name, _ = line.split(';')
            if '.' not in name:
                dirr = True
            if operation != '+':
                if a:
                    continue
                else:
                    name, dire = line.split(';')
                    dire = MINECRAFT+dire
                    if dirr:
                        shutil.move('cosse/'+name, dire)
                    else:
                        if os.path.exists(dire)==False:
                            os.makedirs(dire)
                        shutil.move('cosse/'+name, dire+name)
                    print('Spostato '+name)
            else:
                rest = line[1:]
                name, dire = rest.split(';')
                dire = MINECRAFT+dire
                if a:
                    try:
                        if dirr:
                            shutil.rmtree(dire)
                        else:
                            os.remove(dire+name)
                    except:
                        pass
                if dirr:
                    shutil.move('cosse/'+name, dire)
                else:
                    if os.path.exists(dire)==False:
                        os.makedirs(dire)
                    shutil.move('cosse/'+name, dire+name)
                print('Spostato '+name)
    
    os.remove('cose.zip')
    shutil.rmtree('cosse/')
    if agg or sc:
        tx()
    else:
        fine()

def scarica_mod():
    print("\n\033[92mOra si scaricheranno le mod. premere INVIO")
    input('')
    print("Attendi...\033[0m\n")

    down_error, code = down.sc(MINECRAFT+'mods/')
    down.scarica_file(GITHUB+'ultra_vanilla_2.jar', MINECRAFT+'mods/ultra_vanilla_2.jar')

    if down_error:
        print("\033[91mATTENZIONE: alcune mod non sono state scaricate\033[0m")
        print("Le mod che non sono state scaricate sono:")
        for error in down_error:
            print(error)
        input('\n\033[91mPremere invio per scaricarle dal browser (SE DELLE MOD DA ERRORE 404, CERCATELE E SCARICATELE TE)\033[0m')
        for i in range(len(durl)):
            print(f"{down_error[i]}: {durl[i]}\n")
            webbrowser.open(durl[i])
        input('\n\033[91mPremere invio una volta finite di scaricare\033[0m')

        for i in down_error:
            shutil.move(f"C:\\Users\\{USER}\\Downloads\\{i}", MINECRAFT+'mods/')

    print('Mod scaricate')

    cose(False)

def upt_mod():
    print("\n\033[92mOra si aggiorneranno le mod. premere INVIO")
    input('')
    print("Attendi...\033[0m\n")

    down.confronta_modlist(MINECRAFT+'mods/modlist.json', 'modlist.json')

    with open('differenze.json', "r", encoding="utf-8") as f:
        manifest = json.load(f)
        cancellare = manifest.get("cancellare", [])
        aggiungere = manifest.get("aggiungere", [])

    if cancellare:
        down.cancella_mod(cancellare, MINECRAFT+'mods/')
    shutil.move(MINECRAFT+'mods/mcef-libraries/', './mods/mcef-libraries/')

    # scarica quelle nuove
    if aggiungere:
        down_error = down.aggiungi_mod(aggiungere, MINECRAFT+'mods/')

    if down_error:
        print("\033[91mATTENZIONE: alcune mod non sono state scaricate\033[0m")
        print("Le mod che non sono state scaricate sono:")
        for error in down_error:
            print(error)
        input('\n\033[91mPremere invio per continuare\033[0m')

    print('Mod aggiornate')

    cos = input('\n\033[92mVuoi anche aggiornare cose? (s/n) \033[0m')
    if cos == 's':
        cose(True)
    elif cos == 'n':
        tx()

def rip_mod():
    print("\n\033[92mOra si ripareranno le mod. premere INVIO")
    input('')
    print("Attendi...\033[0m\n")
    down.rip_sposta(MINECRAFT+'mods/')

    shutil.rmtree(MINECRAFT+'mods/')

    # scarica quelle nuove

    down_error, durl = down.rip_down()

    shutil.move('./mods/', MINECRAFT+'mods/')

    if down_error:
        print("\033[91mATTENZIONE: alcune mod non sono state scaricate\033[0m")
        print("Le mod che non sono state scaricate sono:")
        for error in down_error:
            print(error)
        input('\n\033[91mPremere invio per scaricarle dal browser (SE DELLE MOD DA ERRORE 404, CERCATELE E SCARICATELE TE)\033[0m')
        for i in range(len(durl)):
            print(f"{down_error[i]}: {durl[i]}\n")
            webbrowser.open(durl[i])
        input('\n\033[91mPremere invio una volta finite di scaricare\033[0m')

        for i in down_error:
            shutil.move(f"C:\\Users\\{USER}\\Downloads\\{i}", MINECRAFT+'mods/')

    print('Mod riparate')

    tx()

print(USER)
print("Benvenuto nell' installer delle mod")
print("Se devi scaricare le mod scrivi 's'\nSe devi aggiornare scrivi 'a'\nSe devi riparare le mod scrivi 'r'\nSe devi aggiornare la texture pack scrivi 'tx'\nSe devi aggiornare altre cose scrivi 'cose'")
cos = input('')
os.system('cls')
if cos == 's':
    response = requests.get(GITHUB+'modlist.json')
    with open('modlist.json', 'wb') as f:
        f.write(response.content)
    print(f'Scaricato modlist.json')
    sc = True
    scarica_mod()

elif cos == 'a':
    if not os.path.exists(MINECRAFT+'mods/'):
        print("\033[91mLa cartella mods non esiste, quindi scegli 'scaricare'. premi INVIO\033[0m")
        input('')
        sys.exit()
    response = requests.get(GITHUB+'modlist.json')
    with open('modlist.json', 'wb') as f:
        f.write(response.content)
    print(f'Scaricato modlist.json')
    agg = True
    if filecmp.cmp("modlist.json", MINECRAFT+'mods/modlist.json', shallow=False):
        print("\033[92mLe mod sono già aggiornate\033[0m")
        cos = input('\n\033[92mVuoi anche aggiornare cose? (s/n) \033[0m')
        if cos == 's':
            cose(True)
        elif cos == 'n':
            tx()
    upt_mod()

elif cos == 'r':
    response = requests.get(GITHUB+'modlist.json')
    with open('modlist.json', 'wb') as f:
        f.write(response.content)
    print(f'Scaricato modlist.json')
    rip_mod()

elif cos == 'tx':
    tx()

elif cos == 'cose':
    cose(True)
        
# except SystemExit:
#     raise
# except Exception as e:
#     os.system('cls')
#     print("\033[91mERRORE\033[0m")
#     print('\033[91mAPRI "se non worka.bat". se non va neanche quello chiedi a dj \033[0m')
#     input(e)
import os
import requests
os.chdir(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists('./down.py'):
    with open('down.py', 'wb') as f_out:
        response = requests.get('https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/main/download%20mod/mod-vanilla-2/down.py')
        f_out.write(response.content)
import shutil
import sys
import zipfile
import down
import filecmp
import json
import webbrowser


global USER
USER = os.getlogin()
global mod
MINECRAFT = './'
GITHUB = 'https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/main/download%20mod/down/'
mod=False

try:
    def fine():
        os.system('cls')
        shutil.rmtree('__pycache__/')
        os.remove('down.py')
        try:
            os.remove('forge.jar')
            os.remove('forge.jar.log')
            os.remove(MINECRAFT+'mods/manifest.json')
            os.remove('differenze.json')
        except:
            pass
        shutil.move('manifest.json', MINECRAFT+'mods/manifest.json')

        print('\n\033[92mFatto\033[0m')
        input('')
        sys.exit()

    def fix_mod():
        response = requests.get('https://raw.githubusercontent.com/dj2828/Ultra_Vanilla_2/main/download%20mod/down/modlist-server.txt')
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
                    response = requests.get(modlink)
                    with open('./mods/' + nome + '.jar', 'wb') as f:
                        f.write(response.content)
                    print(f'Scaricato {nome}')
        fine()

    def scarica_mod():
        with open('forge.jar', 'wb') as f:
            response = requests.get('https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.4.0/forge-1.20.1-47.4.0-installer.jar')
            f.write(response.content)
        print('Scaricato forge.jar')

        # installa_forge

        print('\033[92mOra comparirà una finestra per installare forge, tu prosegui')
        input('Premi INVIO per iniziare\033[0m ')
        os.system('start '+'./forge.jar')
        print('\n\033[92mUna volta finito premi INVIO\033[0m')
        input('')

        print("\n\033[92mOra si scaricheranno le mod.")
        print("Attendi...\033[0m\n")
        
        down_error, durl = down.sc(MINECRAFT+'mods/')
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

        fix_mod()

    def upt_mod():
        print("\n\033[92mOra si aggiorneranno le mod. premere INVIO")
        input('')
        print("Attendi...\033[0m\n")

        down.confronta_modlist(MINECRAFT+'mods/manifest.json', 'manifest.json')

        with open('differenze.json', "r", encoding="utf-8") as f:
            manifest = json.load(f)
            cancellare = manifest.get("cancellare", [])
            aggiungere = manifest.get("aggiungere", [])

        if cancellare:
            down.cancella_mod(cancellare, MINECRAFT+'mods/')
        
        if os.path.exists(MINECRAFT+'mods/mcef-libraries/'): shutil.move(MINECRAFT+'mods/mcef-libraries/', './mcef-libraries/')
        if os.path.exists(MINECRAFT+'mods/ultra_vanilla_2.jar'): os.remove(MINECRAFT+'mods/ultra_vanilla_2.jar')

        # scarica quelle nuove
        if aggiungere:
            down_error = down.aggiungi_mod(aggiungere, MINECRAFT+'mods/')
        
        if os.path.exists('./mcef-libraries/'): shutil.move('./mcef-libraries/', MINECRAFT+'mods/mcef-libraries/')
        down.scarica_file(GITHUB+'ultra_vanilla_2.jar', MINECRAFT+'mods/ultra_vanilla_2.jar')

        if down_error:
            print("\033[91mATTENZIONE: alcune mod non sono state scaricate\033[0m")
            print("Le mod che non sono state scaricate sono:")
            for error in down_error:
                print(error)
            input('\n\033[91mPremere invio per continuare\033[0m')

        print('Mod aggiornate')

        fix_mod()

    def rip_mod():
        print("\n\033[92mOra si ripareranno le mod. premere INVIO")
        input('')
        print("Attendi...\033[0m\n")
        down.rip_sposta(MINECRAFT+'mods/')

        shutil.rmtree(MINECRAFT+'mods/')

        # scarica quelle nuove

        if not os.path.exists('./mods/ultra_vanilla_2.jar'): down.scarica_file(GITHUB+'ultra_vanilla_2.jar', './mods/ultra_vanilla_2.jar')
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
            fine()
        upt_mod()

    elif cos == 'r':
        response = requests.get(GITHUB+'manifest.json')
        with open('manifest.json', 'wb') as f:
            f.write(response.content)
        print(f'Scaricato manifest.json')
        mod = True
        rip_mod()
except SystemExit:
    raise
except Exception as e:
    os.system('cls')
    print("\033[91mERRORE\033[0m")
    print('\033[91mAPRI "se non worka.bat". se non va neanche quello chiedi a dj \033[0m')
    input(e)
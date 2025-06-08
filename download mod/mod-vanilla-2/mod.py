import os
import shutil
import sys
import requests
import zipfile
import down

global user
user = os.getlogin()
global agg
MINECRAFT = 'C:/Users/'+user+'/AppData/Roaming/.minecraft/'
agg=False

try:
    def fine():
        os.system('cls')
        if agg:
            try:
                os.remove('modlist.json')
                os.remove('forge.jar')
                os.remove('forge-1.20.1-47.4.0-installer.jar.log')
            except:
                pass
            print('\n\033[92mOra prova ad aprire minecarft 1.20.1 forge 47.4.0\033[0m')
            input('')
        sys.exit()

    def tx():
        print('\033[92mScaricamento texturepack\nAttendi...\033[0m')
        response = requests.get('https://github.com/dj2828/sito/releases/download/mod_vanilla_2/Ultra-vanilla-2.zip')
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
        response = requests.get('https://github.com/dj2828/sito/releases/download/mod_vanilla_2/cose.zip')
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
                        try:
                            if dirr:
                                shutil.rmtree(dire)
                            else:
                                os.remove(dire+name)
                        except:
                            pass
                        name, dire = line.split(';')
                        dire = MINECRAFT+''+dire
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
                    dire = MINECRAFT+''+dire
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
        if agg:
            tx()
        else:
            fine()

    def scarica_mod():
        print("\n\033[92mOra si scaricheranno le mod. premere INVIO")
        input('')
        print("Attendi...\033[0m\n")
        with open('forge.jar', 'wb') as f:
            response = requests.get('https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.4.0/forge-1.20.1-47.4.0-installer.jar')
            f.write(response.content)
        print('Scaricato forge.jar')
        
        down.sc(MINECRAFT+'mods/')
        down.scarica_file('https://github.com/dj2828/sito/releases/download/mod_vanilla_2/ultra_vanilla_2.jar', MINECRAFT+'mods/ultra_vanilla_2.jar')

        print("\033[92mPremere INVIO\033[0m")
        input('')

        # installa_forge

        print('\033[92mOra comparirà una finestra per installare forge, tu prosegui')
        input('Premi INVIO per iniziare\033[0m ')
        os.system('start '+'C:/Users/'+user+'/Downloads/forge-1.20.1-47.4.0-installer.jar')
        print('\n\033[92mUna volta finito premi INVIO\033[0m')
        input('')

        print('Mod scaricate')

        cose(False)

    def upt_mod():
        print("\n\033[92mOra si aggiorneranno le mod. premere INVIO")
        input('')
        print("Attendi...\033[0m\n")
        down.upt_sposta(MINECRAFT+'mods/')
        shutil.move(MINECRAFT+'mods/mcef-libraries/', './mods/mcef-libraries/')

        shutil.rmtree(MINECRAFT+'mods/')

        # scarica quelle nuove

        down.upt_down()
        
        shutil.move('./mods/', MINECRAFT+'mods/')

        print('Mod aggiornate')

        cos = input('\n\033[92mVuoi anche aggiornare cose? (s/n) \033[0m')
        if cos == 's':
            cose(True)
        elif cos == 'n':
            tx()

    print(user)
    print("Benvenuto nell' installer delle mod")
    print("Se devi scaricare le mod scrivi 's'\nSe devi aggiornare scrivi 'a'\nSe devi aggiornare la texture pack scrivi 'tx'\nSe devi aggiornare altre cose scrivi 'cose'")
    cos = input('')
    os.system('cls')
    if cos == 's':
        response = requests.get('https://github.com/dj2828/sito/releases/download/mod_vanilla_2/modlist.json')
        with open('modlist.json', 'wb') as f:
            f.write(response.content)
        print(f'Scaricato modlist.json')

        while os.path.exists(MINECRAFT+'mods'):
            print('\033[91mLa cartella mods esiste ancora, rinominala o cancellala. premi INVIO\033[0m')
            input('')
            os.system('start '+MINECRAFT+'')
            print('Una volta fatto premi INVIO')
            input('')
        os.makedirs(MINECRAFT+'mods/')

        agg = True
        scarica_mod()

    elif cos == 'a':
        if os.path.exists(MINECRAFT+'mods/') == False:
            print("\033[91mLa cartella mods non esiste, quindi scegli 'scaricare'. premi INVIO\033[0m")
            input('')
            sys.exit()
        response = requests.get('https://github.com/dj2828/sito/releases/download/mod_vanilla_2/modlist.json')
        with open('modlist.json', 'wb') as f:
            f.write(response.content)
        print(f'Scaricato modlist.json')
        agg = True
        upt_mod()

    elif cos == 'tx':
        tx()

    elif cos == 'cose':
        cose(True)
        
except SystemExit:
    raise
except:
    os.system('cls')
    print("\033[91mERRORE\033[0m")
    input('\033[91mAPRI "se non worka.bat". se non va neanche quello chiedi a dj \033[0m')
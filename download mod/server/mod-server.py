import os
import shutil
import sys
import requests

global user

def fine():
    os.remove('modlist-server.txt')
    # os.remove('cose.zip')
    # shutil.rmtree('cosse/')

    print('\nFatto')
    input('')
    sys.exit()


user = os.getlogin()

response = requests.get('https://github.com/dj2828/sito/releases/download/mod_vanilla_2/modlist-server.txt')
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
            if os.path.exists('./mods/'+nome):
                os.remove('./mods/'+nome)
                print(f'Cancellato {nome}')
        else:
            nome, modlink = line.split(';')
            response = requests.get(modlink)
            with open('./mods/' + nome + '.jar', 'wb') as f:
                f.write(response.content)
            print(f'Scaricato {nome}')

fine()
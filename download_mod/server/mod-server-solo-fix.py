# Questo script sistema le mod per il server ma non le scarica

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
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
            response = requests.get(modlink)
            with open('./mods/' + nome + '.jar', 'wb') as f:
                f.write(response.content)
            print(f'Scaricato {nome}')

fine()
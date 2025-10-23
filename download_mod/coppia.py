import pyperclip

global giacopp
giacopp = ''

print(f"Lo script è in esecuzione. Premi CTRL+C per interromperlo.")

# Apri il file in modalità append
with open('a.txt', 'a') as file:
    while True:
        # Leggi il testo dal clipboard
        copied_text = pyperclip.paste().strip()
            
        if copied_text and giacopp!=copied_text:
            # Scrivi il testo nel file
            file.write(copied_text + '\n')  # Aggiungi un newline alla fine per separare i testi
            print(copied_text)
            giacopp = copied_text
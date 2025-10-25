#!/bin/bash

# =========================================================================
# SCRIPT DI AVVIO E MONITORAGGIO SERVER MINECRAFT
# Con gestione argomenti da file: user_jvm_args.txt e options.txt
# =========================================================================

# --- CONFIGURAZIONE FILE E VARIABILI ---
SERVER_JAR="tuo_server.jar" 

# File da cui leggere gli argomenti JVM (RAM, Garbage Collector, ecc.)
JVM_ARGS_FILE="user_jvm_args.txt"

# File da cui leggere gli argomenti del server (es. nogui)
SERVER_OPTIONS_FILE="options.txt"

# Tempo di aggiornamento per il monitoraggio della CPU (in secondi)
WATCH_INTERVAL=5

# --- FUNZIONE: CARICA ARGOMENTI DA FILE ---
function load_args() {
    # Legge gli argomenti JVM dal file
    if [ -f "$JVM_ARGS_FILE" ]; then
        JVM_ARGS=$(cat "$JVM_ARGS_FILE")
    else
        echo "ATTENZIONE: File '$JVM_ARGS_FILE' non trovato. Usando argomenti RAM di default."
        # Impostiamo argomenti RAM di base se il file non esiste
        JVM_ARGS="-Xms1024M -Xmx4G"
    fi

    # Legge gli argomenti del server dal file
    if [ -f "$SERVER_OPTIONS_FILE" ]; then
        SERVER_ARGS=$(cat "$SERVER_OPTIONS_FILE")
    else
        echo "ATTENZIONE: File '$SERVER_OPTIONS_FILE' non trovato. Usando 'nogui' di default."
        SERVER_ARGS="nogui"
    fi
}

# --- VERIFICA PREREQUISITI ---

function check_prerequisites() {
    echo "Verifica dei prerequisiti..."
    
    if ! command -v java &> /dev/null; then
        echo "ERRORE: Java Runtime Environment (JRE) non trovato."
        exit 1
    fi
    
    if ! command -v sensors &> /dev/null; then
        echo "ATTENZIONE: Il comando 'sensors' (lm-sensors) non e' installato. Installalo per monitorare la CPU."
    fi
    
    if [ ! -f "$SERVER_JAR" ]; then
        echo "ERRORE: Il file del server JAR non e' stato trovato: $SERVER_JAR"
        echo "Modifica la variabile SERVER_JAR nello script."
        exit 1
    fi
}

# --- FUNZIONE DI MONITORAGGIO CPU ---

function monitor_cpu() {
    echo "Avvio monitoraggio CPU in tempo reale (ogni $WATCH_INTERVAL secondi)..."
    echo "Premi CTRL+C per tornare al menu principale."
    sleep 1
    
    if command -v sensors &> /dev/null; then
        watch -n $WATCH_INTERVAL sensors
    else
        echo "Il monitoraggio della CPU e' disabilitato perche' lm-sensors non e' installato."
        read -p "Premi Invio per continuare..."
    fi
}

# --- FUNZIONE DI AVVIO SERVER ---

function start_server() {
    load_args # Ricarica gli argomenti prima di ogni avvio
    
    echo "Argomenti JVM: $JVM_ARGS"
    echo "Argomenti Server: $SERVER_ARGS"
    echo "Avvio del server Minecraft in una sessione 'screen'..."
    
    # Avvia il server usando tutti gli argomenti caricati
    screen -dmS minecraft java $JVM_ARGS -jar "$SERVER_JAR" $SERVER_ARGS
    
    echo "Server avviato nella sessione screen 'minecraft'."
    echo "Per entrare nella console: screen -r minecraft"
}

# --- FUNZIONE MENU PRINCIPALE ---

function main_menu() {
    while true; do
        clear
        echo "=========================================================="
        echo "         MENU SERVER MINECRAFT & MONITORAGGIO"
        echo "=========================================================="
        echo "1) Avvia Server Minecraft (in background con screen)"
        echo "2) Entra nella Console del Server (screen -r minecraft)"
        echo "3) Monitora Temperatura CPU (tempo reale)"
        echo "4) Visualizza Utilizzo CPU/RAM (htop)"
        echo "0) Esci dallo Script"
        echo "=========================================================="
        
        read -p "Scegli un'opzione: " choice
        
        case $choice in
            1)
                start_server
                read -p "Premi Invio per tornare al menu..."
                ;;
            2)
                screen -r minecraft
                ;;
            3)
                monitor_cpu
                ;;
            4)
                if command -v htop &> /dev/null; then
                    htop
                else
                    echo "htop non e' installato. Installa con: sudo apt install htop"
                    read -p "Premi Invio per continuare..."
                fi
                ;;
            0)
                echo "Uscita dallo script. Arrivederci!"
                exit 0
                ;;
            *)
                echo "Scelta non valida. Riprova."
                read -p "Premi Invio per continuare..."
                ;;
        esac
    done
}

# --- ISTRUZIONI PER LA CREAZIONE DEI FILE ---

echo ""
echo "=========================================================="
echo "   PREPARAZIONE DEI FILE DI CONFIGURAZIONE"
echo "=========================================================="
echo "Crea i seguenti file nella stessa directory dello script:"
echo ""
echo "1. File: $JVM_ARGS_FILE"
echo "   Contiene le opzioni JVM (es. RAM, Garbage Collector)."
echo "   Esempio di contenuto:"
echo '   -Xms4G -Xmx8G -XX:+UseG1GC -XX:+ParallelRefProcEnabled'
echo ""
echo "2. File: $SERVER_OPTIONS_FILE"
echo "   Contiene gli argomenti specifici del server (es. nogui)."
echo "   Esempio di contenuto (una riga):"
echo '   nogui'
echo "=========================================================="
read -p "Premi Invio per continuare con il menu..."

# --- ESECUZIONE ---
check_prerequisites
main_menu
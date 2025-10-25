#!/bin/bash

# =========================================================================
# SCRIPT DI AVVIO E MONITORAGGIO SERVER MINECRAFT (INTEGRATO CON run.sh)
# AGGIUNTA: Opzione di Spegnimento Sicuro del Server
# =========================================================================

# --- CONFIGURAZIONE FILE E VARIABILI ---
RUN_SCRIPT="./run.sh"
SERVER_ARGS="nogui"
WATCH_INTERVAL=2

# --- FUNZIONE: VERIFICA STATO SERVER ---

function check_server_status() {
    if screen -list | grep -q "minecraft"; then
        echo "STATO: Il server Minecraft e' ATTIVO (nella sessione 'minecraft')."
    else
        echo "STATO: Il server Minecraft e' OFFLINE."
    fi
}

# --- VERIFICA PREREQUISITI ---

function check_prerequisites() {
    echo "Verifica dei prerequisiti..."
    
    if [ ! -x "$RUN_SCRIPT" ]; then
        echo "ERRORE: Lo script di avvio '$RUN_SCRIPT' non e' stato trovato o non e' eseguibile."
        echo "Assicurati che sia nella stessa directory e che abbia i permessi di esecuzione (chmod +x $RUN_SCRIPT)."
        exit 1
    fi
    
    if ! command -v sensors &> /dev/null; then
        echo "ATTENZIONE: 'sensors' (lm-sensors) non e' installato. Installalo con: sudo apt install lm-sensors"
    fi
    
    if ! command -v screen &> /dev/null; then
        echo "ATTENZIONE: 'screen' non e' installato. Installalo con: sudo apt install screen"
    fi
}

# --- FUNZIONE DI SPEGNIMENTO SICURO (NUOVA) ---

function stop_server_safe() {
    if screen -list | grep -q "minecraft"; then
        echo "Invio del comando '/stop' alla console del server 'minecraft'..."
        # Invia il comando '/stop' alla sessione screen chiamata 'minecraft'
        screen -S minecraft -X stuff "say Shutting down in 10 seconds...$(echo -e '\015')"
        sleep 10
        screen -S minecraft -X stuff "stop$(echo -e '\015')"
        
        echo "Comando inviato. Attendi che il server si spenga completamente..."
        # Attendiamo un po' e verifichiamo che la sessione sia terminata
        sleep 15
        
        if screen -list | grep -q "minecraft"; then
            echo "Il server e' ancora attivo. Potrebbe essere necessario spegnerlo manualmente."
        else
            echo "Server Minecraft spento con successo."
        fi
    else
        echo "Il server non sembra essere attivo. Nessuna azione intrapresa."
    fi
}

# --- FUNZIONE DI MONITORAGGIO CPU (Invariata) ---

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

# --- FUNZIONE DI AVVIO SERVER (Invariata) ---

function start_server() {
    check_server_status
    if screen -list | grep -q "minecraft"; then
        echo "Il server e' gia' attivo. Per spegnerlo, usa l'Opzione 5."
        return
    fi

    echo "Avvio del server Minecraft usando $RUN_SCRIPT e argomenti: $SERVER_ARGS"
    
    screen -dmS minecraft $RUN_SCRIPT $SERVER_ARGS
    
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
        check_server_status
        echo "----------------------------------------------------------"
        echo "1) Avvia Server Minecraft (in background)"
        echo "2) Entra nella Console del Server (screen -r minecraft)"
        echo "3) Monitora Temperatura CPU (tempo reale)"
        echo "4) Visualizza Utilizzo CPU/RAM (htop)"
        echo "5) Spegni Server (sicuro - invia /stop)"
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
                    echo "htop non e' installato. Installalo con: sudo apt install htop"
                    read -p "Premi Invio per continuare..."
                fi
                ;;
            5)
                stop_server_safe
                read -p "Premi Invio per tornare al menu..."
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

# --- ESECUZIONE ---
check_prerequisites
main_menu
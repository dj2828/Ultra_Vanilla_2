@echo off
setlocal enabledelayedexpansion

:: =========================================================================
:: SCRIPT DI AVVIO E MONITORAGGIO SERVER MINECRAFT (PER WINDOWS)
:: ADATTAMENTO: Usa 'start' per l'avvio e 'RCON' per lo spegnimento sicuro.
:: =========================================================================


:: --- CONFIGURAZIONE FILE E VARIABILI ---

REM Adatta questo al nome del tuo script di avvio
set "RUN_SCRIPT=run.bat"
REM Argomenti da passare allo script (es. nogui)
set "SERVER_ARGS=nogui"
REM Titolo della finestra del server, usato per controllarne lo stato
set "WINDOW_TITLE=Server Minecraft"

REM --- CONFIGURAZIONE RCON (NECESSARIA PER SPEGNIMENTO SICURO) ---
REM Assicurati che RCON sia abilitato in 'server.properties' (enable-rcon=true)
set "RCON_HOST=127.0.0.1"
set "RCON_PORT=25575"
set "RCON_PASSWORD=lamia_password_rcon"

REM Percorso del client RCON (scarica 'mcrcon.exe' e mettilo qui)
set "RCON_CLIENT=mcrcon.exe"


:: --- FUNZIONE: VERIFICA STATO SERVER ---
:check_server_status
    REM Controlliamo se esiste una finestra con il titolo specificato
    REM e se al suo interno sta girando java (il server)
    tasklist /FI "WINDOWTITLE eq %WINDOW_TITLE%" | findstr /i "java.exe" >nul 2>nul
    
    if %ERRORLEVEL% == 0 (
        set "SERVER_STATUS=ATTIVO"
    ) else (
        set "SERVER_STATUS=OFFLINE"
    )
    goto :EOF


:: --- VERIFICA PREREQUISITI ---
:check_prerequisites
    echo Verifica dei prerequisiti...
    
    if not exist "%RUN_SCRIPT%" (
        echo ERRORE: Lo script di avvio '%RUN_SCRIPT%' non e' stato trovato.
        echo Assicurati che sia nella stessa directory.
        pause
        exit /b 1
    )
    
    if not exist "%RCON_CLIENT%" (
        echo.
        echo ATTENZIONE: Client RCON '%RCON_CLIENT%' non trovato.
        echo Lo spegnimento sicuro (Opzione 5) non funzionera'.
        echo Scaricalo (cerca 'mcrcon') e mettilo in questa cartella.
        pause
    )
    
    where wmic >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo "ATTENZIONE: 'wmic' non trovato. Il monitoraggio temperature non funzionera'."
    )
    
    where resmon >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo "ATTENZIONE: 'resmon' non trovato. Il monitoraggio risorse non funzionera'."
    )
    echo Prerequisiti verificati.
    echo.
    goto :EOF


:: --- FUNZIONE DI SPEGNIMENTO SICURO (con RCON) ---
:stop_server_safe
    call :check_server_status
    if "%SERVER_STATUS%"=="OFFLINE" (
        echo Il server e' gia' offline. Nessuna azione intrapresa.
        goto :EOF
    )

    if not exist "%RCON_CLIENT%" (
        echo ERRORE: Client RCON non trovato. Impossibile spegnere in modo sicuro.
        goto :EOF
    )

    echo "Invio del comando '/stop' alla console del server via RCON..."
    
    REM Invia il messaggio di avviso
    "%RCON_CLIENT%" -H %RCON_HOST% -P %RCON_PORT% -p %RCON_PASSWORD% "say Shutting down in 10 seconds..." >nul
    
    REM Attende 10 secondi (timeout e' l'equivalente di 'sleep')
    timeout /t 10 /nobreak >nul
    
    REM Invia il comando di stop
    "%RCON_CLIENT%" -H %RCON_HOST% -P %RCON_PORT% -p %RCON_PASSWORD% "stop" >nul
    
    echo "Comando inviato. Attendi che il server si spenga completamente..."
    timeout /t 5 /nobreak >nul
    call :check_server_status
    echo "Stato attuale: %SERVER_STATUS%"
    goto :EOF


:: --- FUNZIONE DI MONITORAGGIO CPU (con WMIC) ---
:monitor_cpu
    echo "Avvio monitoraggio Temperatura (tramite WMIC)..."
    echo "Premi CTRL+C per tornare al menu principale."
    echo "NOTA: I valori potrebbero non essere precisi o disponibili."
    sleep 1
    
    cls
    :watch_loop
    cls
    echo "--- Monitoraggio Temperature (Premi CTRL+C per uscire) ---"
    echo Data: %DATE% %TIME%
    echo.
    REM Questo comando e' l'equivalente di 'sensors' piu' vicino in batch, 
    REM ma spesso non da' la temperatura della CPU.
    wmic /namespace:\\root\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature
    echo.
    echo (Le temperature sono in Kelvin / 10. Esempio: 3101 = 310.1 K = 37 C)
    
    REM Equivalente di 'watch -n 2'
    timeout /t 2 /nobreak >nul
    goto :watch_loop


:: --- FUNZIONE DI AVVIO SERVER (con 'start') ---
:start_server
    call :check_server_status
    if "%SERVER_STATUS%"=="ATTIVO" (
        echo "Il server e' gia' attivo. Per spegnerlo, usa l'Opzione 5."
        goto :EOF
    )

    echo "Avvio del server Minecraft in una NUOVA FINESTRA..."
    echo "Usa %RUN_SCRIPT% con argomenti: %SERVER_ARGS%"
    
    REM 'start' avvia il comando in una nuova finestra
    REM Il primo argomento "" e' il titolo della finestra (che usiamo per il check)
    start "%WINDOW_TITLE%" %RUN_SCRIPT% %SERVER_ARGS%
    
    echo "Server avviato nella finestra '%WINDOW_TITLE%'."
    echo "Per interagire con la console, usa quella finestra."
    goto :EOF


:: --- FUNZIONE MENU PRINCIPALE ---
:main_menu
    cls
    echo ==========================================================
    echo          MENU SERVER MINECRAFT & MONITORAGGIO (WINDOWS)
    echo ==========================================================
    call :check_server_status
    echo STATO: Il server Minecraft e' %SERVER_STATUS%.
    echo ----------------------------------------------------------
    echo 1) Avvia Server Minecraft (in una nuova finestra)
    echo 2) Apri Console Server (Interagisci con la finestra)
    echo 3) Monitora Temperatura CPU (con WMIC)
    echo 4) Visualizza Utilizzo CPU/RAM (Monitoraggio Risorse)
    echo 5) Spegni Server (sicuro - via RCON)
    echo 0) Esci dallo Script
    echo ==========================================================
    
    set "choice="
    set /p choice="Scegli un'opzione: "
    
    if "%choice%"=="1" (
        call :start_server
        pause
    ) else if "%choice%"=="2" (
        echo.
        echo "AZIONE NON NECESSARIA:"
        echo "La console e' la finestra separata che si e' aperta"
        echo "quando hai avviato il server (titolo: '%WINDOW_TITLE%')."
        echo "Fai clic su quella finestra per digitare i comandi."
        pause
    ) else if "%choice%"=="3" (
        call :monitor_cpu
    ) else if "%choice%"=="4" (
        echo "Avvio di 'Monitoraggio Risorse' (resmon)..."
        start resmon
    ) else if "%choice%"=="5" (
        call :stop_server_safe
        pause
    ) else if "%choice%"=="0" (
        echo "Uscita dallo script. Arrivederci!"
        goto :exit_script
    ) else (
        echo "Scelta non valida. Riprova."
        pause
    )
    goto :main_menu

:: --- ESECUZIONE ---
call :check_prerequisites
call :main_menu

:exit_script
endlocal
exit /b

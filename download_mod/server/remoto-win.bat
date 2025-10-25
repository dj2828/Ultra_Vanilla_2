@echo off
setlocal enabledelayedexpansion

:: =========================================================================
:: SCRIPT DI GESTIONE REMOTA SERVER MINECRAFT (PER WINDOWS)
:: Questo script gira sul tuo PC MAIN e comanda il PC SERVER.
:: =Good-Loop
:: =========================================================================

:: --- CONFIGURAZIONE REMOTA ---

REM L'IP (o nome host) del PC SERVER su cui gira Minecraft
set "SERVER_IP=192.168.1.50"

REM === CONFIGURAZIONE AVVIO/MONITORAGGIO (Richiede permessi Admin) ===
REM Per avviare/controllare lo stato, servono credenziali ADMIN del PC SERVER.
REM !! ATTENZIONE !! Salvare la password qui e' INSICURO.
REM Se lasci vuoto, te lo chiedera' ogni volta (piu' sicuro).
set "SERVER_ADMIN_USER=NomeAdminSulServer"
set "SERVER_ADMIN_PASS=PasswordAdminSulServer"

REM Il percorso *completo* allo script run.bat SUL PC SERVER
set "SERVER_PATH=C:\MinecraftServer\run.bat"
set "SERVER_ARGS=nogui"


REM === CONFIGURAZIONE RCON (Per comandi /stop, /say, etc.) ===
REM Assicurati che RCON sia abilitato in 'server.properties' sul server
set "RCON_HOST=%SERVER_IP%"
set "RCON_PORT=25575"
set "RCON_PASSWORD=LaTuaPasswordSegreta"

REM Metti mcrcon.exe nella stessa cartella di questo script
set "RCON_CLIENT=mcrcon.exe"


:: --- VARIABILI DI STATO ---
set "SERVER_STATUS=SCONOSCIUTO"
set "AUTH_STRING="
if not "%SERVER_ADMIN_PASS%"=="" (
    set "AUTH_STRING=/U %SERVER_ADMIN_USER% /P %SERVER_ADMIN_PASS%"
) else (
    set "AUTH_STRING=/U %SERVER_ADMIN_USER%"
)


:: --- FUNZIONE: VERIFICA STATO SERVER (REMOTA) ---
:check_server_status
    echo Controllo stato server su %SERVER_IP%...
    
    REM Check 1: Il processo java e' attivo? (Usa tasklist remoto)
    tasklist /S %SERVER_IP% %AUTH_STRING% 2>nul | findstr /i "java.exe" >nul
    
    if %ERRORLEVEL% NEQ 0 (
        set "SERVER_STATUS=OFFLINE (Processo non trovato)"
        goto :EOF
    )
    
    REM Check 2: Il processo e' attivo, ma RCON risponde?
    echo "Processo Java trovato. Tento connessione RCON..."
    "%RCON_CLIENT%" -H %RCON_HOST% -P %RCON_PORT% -p %RCON_PASSWORD% "list" >nul 2>nul
    
    if %ERRORLEVEL% == 0 (
        set "SERVER_STATUS=ATTIVO (RCON OK)"
    ) else (
        set "SERVER_STATUS=ATTIVO (RCON NON RISPONDE! - Forse bloccato?)"
    )
    goto :EOF


:: --- VERIFICA PREREQUISITI (LOCALE) ---
:check_prerequisites
    echo Verifica dei prerequisiti (sul tuo PC Main)...
    
    if not exist "%RCON_CLIENT%" (
        echo.
        echo ERRORE: Client RCON '%RCON_CLIENT%' non trovato.
        echo Scaricalo (cerca 'mcrcon.exe') e mettilo in questa cartella.
        pause
        exit /b 1
    )
    echo Prerequisiti OK.
    echo.
    goto :EOF


:: --- FUNZIONE DI SPEGNIMENTO SICURO (con RCON) ---
:stop_server_safe
    call :check_server_status
    if "%SERVER_STATUS%"=="OFFLINE (Processo non trovato)" (
        echo Il server e' gia' offline.
        goto :EOF
    )

    echo "Invio del comando '/stop' a %RCON_HOST% via RCON..."
    
    "%RCON_CLIENT%" -H %RCON_HOST% -P %RCON_PORT% -p %RCON_PASSWORD% "say Spegnimento server tra 10 secondi..." >nul
    timeout /t 10 /nobreak >nul
    
    REM Invia il comando di stop
    "%RCON_CLIENT%" -H %RCON_HOST% -P %RCON_PORT% -p %RCON_PASSWORD% "stop" >nul
    
    echo "Comando inviato. Attendi che il server si spenga..."
    timeout /t 5 /nobreak >nul
    goto :EOF


:: --- FUNZIONE DI AVVIO SERVER (REMOTA con WMIC) ---
:start_server_remote
    call :check_server_status
    if not "%SERVER_STATUS%"=="OFFLINE (Processo non trovato)" (
        echo "Il server sembra essere gia' attivo (%SERVER_STATUS%)."
        goto :EOF
    )

    echo "Tentativo di avvio processo remoto su %SERVER_IP%..."
    echo "Comando: %SERVER_PATH% %SERVER_ARGS%"
    
    REM Usiamo WMIC per creare un processo sul computer remoto
    wmic /NODE:%SERVER_IP% %AUTH_STRING% process call create "%SERVER_PATH% %SERVER_ARGS%"
    
    if %ERRORLEVEL% EQU 0 (
        echo "Comando di avvio inviato con successo."
        echo "Attendi circa 30 secondi che il server si avvii..."
    ) else (
        echo "ERRORE: Impossibile avviare il processo."
        echo "Controlla credenziali, IP, percorso e firewall (WMI)."
    )
    goto :EOF

:: --- FUNZIONE DI MONITORAGGIO CPU (REMOTA con WMIC) ---
:monitor_cpu_remote
    echo "Avvio monitoraggio CPU REMOTO su %SERVER_IP% (Premi CTRL+C per uscire)..."
    sleep 1
    
    :watch_loop
    cls
    echo "--- Monitoraggio REMOTO di %SERVER_IP% (Premi CTRL+C) ---"
    echo Data: %DATE% %TIME%
    echo.
    echo Carico CPU:
    wmic /NODE:%SERVER_IP% %AUTH_STRING% cpu get loadpercentage
    echo.
    echo Temperatura (Spesso non disponibile):
    wmic /NODE:%SERVER_IP% %AUTH_STRING% /namespace:\\root\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature
    
    timeout /t 3 /nobreak >nul
    goto :watch_loop


:: --- FUNZIONE INVIO COMANDO RCON ---
:send_rcon_command
    echo "Scrivi il comando da inviare (senza /). Digita 'exit' per uscire."
    :rcon_prompt
    set "rcon_cmd="
    set /p rcon_cmd="RCON (%RCON_HOST%): "
    
    if /i "%rcon_cmd%"=="exit" goto :EOF
    if "%rcon_cmd%"=="" goto :rcon_prompt
    
    echo "Invio: %rcon_cmd%"
    "%RCON_CLIENT%" -H %RCON_HOST% -P %RCON_PORT% -p %RCON_PASSWORD% "%rcon_cmd%"
    echo.
    goto :rcon_prompt


:: --- FUNZIONE MENU PRINCIPALE ---
:main_menu
    cls
    echo ==========================================================
    echo      PANNELLO DI CONTROLLO REMOTO MINECRAFT
    echo ==========================================================
    echo Server: %SERVER_IP%
    call :check_server_status
    echo Stato:  %SERVER_STATUS%
    echo ----------------------------------------------------------
    echo 1) Avvia Server (Remoto)
    echo 2) Spegni Server (Sicuro - RCON)
    echo 3) Invia Comando Manuale (RCON)
    echo 4) Monitora CPU Server (Remoto - WMIC)
    echo 5) Controlla Stato (Aggiorna)
    echo 0) Esci
    echo ==========================================================
    
    set "choice="
    set /p choice="Scegli un'opzione: "
    
    if "%choice%"=="1" (
        call :start_server_remote
        pause
    ) else if "%choice%"=="2" (
        call :stop_server_safe
        pause
    ) else if "%choice%"=="3" (
        call :send_rcon_command
    ) else if "%choice%"=="4" (
        call :monitor_cpu_remote
    ) else if "%choice%"=="5" (
        goto :main_menu
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

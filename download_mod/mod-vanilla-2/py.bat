@echo off
title Controllo e installazione Python
echo =====================================
echo     Controllo installazione Python
echo =====================================
echo.

:: 1. CONTROLLO E RECUPERO VERSIONE (USARE 'py' E REINDIRIZZAMENTO ROBUSTO)
:: Tenta di eseguire 'py --version'. Se riesce (errorlevel=0), Python e' installato.
py --version >nul 2>&1
if %errorlevel%==0 (
    
    :: Python e' installato. Recupera la versione in modo robusto.
    :: 'py -V' stampa solo il numero (es. 3.12.0) che e' piu' facile da catturare.
    for /f "delims=" %%a in ('py -V') do set PYVER=%%a
    echo Python e' gia' installato! Versione: %PYVER%

    :: Salta l'installazione e vai alla configurazione.
    goto Configure
) else (
    echo Python non e' installato o non e' nel PATH (anche dopo il riavvio). Avvio installazione...
    
    :: 2. CONTROLLO WINGET
    winget --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Errore: winget non trovato. Installa manualmente Python da https://python.org
        pause
        exit /b 1
    )

    :: 3. INSTALLAZIONE CON WINGET
    echo.
    echo Installazione di Python tramite winget...
    winget install -e --id Python.Python.3.12 -h
    if %errorlevel% neq 0 (
        echo Errore durante l'installazione di Python.
        pause
        exit /b 1
    )

    :: 4. ISTRUZIONI PER IL RIAVVIO DOPO L'INSTALLAZIONE
    echo.
    echo ********************************************************
    echo INSTALLAZIONE COMPLETATA.
    echo E' necessario RIAVVIARE QUESTA FINESTRA DEL TERMINALE
    echo per rendere il comando 'py' disponibile.
    echo RIESEGUIRE LO SCRIPT DOPO IL RIAVVIO.
    echo ********************************************************
    pause
    exit /b 0
)

:Configure
echo.
echo =====================================
echo     Configurazione ambiente Python
echo =====================================

:: Abilita colori console
reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul

:: Installa moduli richiesti (usa 'py -m pip' che e' piu' affidabile di 'pip')
echo Installazione moduli Python (requests, tqdm)...
py -m pip install requests tqdm

echo.
echo Tutto pronto! Python e i moduli necessari sono installati.
pause
exit /b 0
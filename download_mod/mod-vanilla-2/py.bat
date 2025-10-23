@echo off
title Controllo e installazione Python
echo =====================================
echo     Controllo installazione Python
echo =====================================
echo.

:: Controlla se Python è installato
python --version >nul 2>&1
if %errorlevel%==0 (
    for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do set PYVER=%%a
    echo Python è già installato! Versione: %PYVER%
) else (
    echo Python non è installato. Avvio installazione...
    
    :: Controlla se winget è disponibile
    winget --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Errore: winget non trovato. Installa manualmente Python da https://python.org
        pause
        exit /b 1
    )

    :: Installa Python con winget (ultima versione stabile)
    echo.
    echo Installazione di Python tramite winget...
    winget install -e --id Python.Python.3.12 -h
    if %errorlevel% neq 0 (
        echo Errore durante l'installazione di Python.
        pause
        exit /b 1
    )

    echo.
    echo Installazione completata. Aggiornamento PATH...
    setx PATH "%PATH%;%LocalAppData%\Programs\Python\Python312\Scripts;%LocalAppData%\Programs\Python\Python312\"
)

echo.
echo =====================================
echo     Configurazione ambiente Python
echo =====================================

:: Abilita colori console
reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul

:: Installa moduli richiesti
echo Installazione moduli Python (requests, tqdm)...
py -m pip install --upgrade pip >nul
py -m pip install requests tqdm

echo.
echo Tutto pronto! Python e i moduli necessari sono installati.
pause
exit /b 0

@echo off
set /p "scelta=Hai ATlauncher? (s/n): "

if /i "%scelta%"=="s" (
    python "mod per chi ha ATlauncher.py"
) else (
    python mod.py
)
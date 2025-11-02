@echo off

reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f
py -m pip install requests tqdm

pause
exit /b 0
@echo off
set LOG_DIR=C:\Users\USER\Desktop\Igor\Runs\DT\Liam_test\Code\logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set LOG_FILE=%LOG_DIR%\filter_log.txt

echo. >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"
echo Run started at: %date% %time% >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"

powershell.exe -ExecutionPolicy Bypass -File "C:\Users\USER\Desktop\Igor\Runs\DT\Liam_test\Code\filtering_loop.ps1" >> "%LOG_FILE%" 2>&1 
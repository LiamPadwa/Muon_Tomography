@echo off

set PYTHON_SCRIPT=C:\Users\Jerusalem2\Desktop\Cronjob_code\Start_runs\start_stop_run.py
set LOG_FILE=C:\Users\Jerusalem2\Desktop\Cronjob_code\Start_runs\python_task_log.txt

powershell.exe -ExecutionPolicy Bypass -Command ^
    "& python '%PYTHON_SCRIPT%' --command STOP" >> "%LOG_FILE%" 2>&1

powershell.exe -ExecutionPolicy Bypass -Command ^
    "& python '%PYTHON_SCRIPT%' --command START" >> "%LOG_FILE%" 2>&1


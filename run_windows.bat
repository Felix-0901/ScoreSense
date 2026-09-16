@echo off
cd /d %~dp0
python main.py web --host 127.0.0.1 --port 8000
pause

@echo off
echo Installing required packages
@pip install -r requirements.txt
@python app.py
echo Program crashed/quit
pause()

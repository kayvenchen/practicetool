@echo off
echo Installing required packages
@pip install -r requirements.txt
@C:
@cd C:\Python36\Scripts\
@pip install -r S:\18300\practicetool\requirements.txt
echo Finished installing any required packages
@python routes.py
@cd C:\Python36\
@python S:\18300\practicetool\app.py
echo Program crashed/quit
pause()

@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated.
echo Installing Dependencies...
call pip install -r requirements.txt
echo Running Django server...
python manage.py runserver
echo Django server stopped. Please close the command prompt window to exit.
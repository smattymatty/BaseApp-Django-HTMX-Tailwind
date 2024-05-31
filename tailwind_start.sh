#!/bin/bash
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated."
echo "Installing Dependencies..."
pip install -r requirements.txt
echo "Running 'python manage.py' command..."
python manage.py tailwind start
read -p "Press [Enter] key to continue..."

echo "Activating virtual environment..."
source venv/bin/activate 
echo "Virtual environment activated."
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Running Django server..."
python manage.py runserver

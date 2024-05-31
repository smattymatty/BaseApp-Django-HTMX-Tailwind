# credentials.py (remove _example from the filename)

# SECURITY WARNING:
# Replace the following placeholder with a strong, unique secret key for your Django project.
# You can generate one using:
#     python -c "import secrets; print(secrets.token_urlsafe(50))"
SECRET_KEY = ''  # Replace this with your actual secret key

# Database configuration
# NOTE: This is a sample SQLite configuration for initial setup and testing.
# For production or more robust development, replace it with your actual database settings (e.g., PostgreSQL).
DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'mydatabase',  # Replace with your database name (optional)
}

# Optional: Add more credentials here for other services or APIs
# Example:
# API_KEY = 'your_api_key'

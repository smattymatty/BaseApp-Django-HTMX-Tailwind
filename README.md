# Base Django App

I'm making this for fun, it's not finished but feel free to use it, don't question my old messy code that I plan on refactoring later :)

## Installation and Setup
1. Clone the repository to your local machine:
```bash
git clone https://github.com/smattymatty/Base-Django-HTMX-Tailwind
cd base-django-app
```
2. Create a virtual environment (recommended):
```bash
python -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate it (Linux/macOS)
venv\Scripts\activate  # Activate it (Windows)

```
3. Install Dependencies:
```bash
pip install -r requirements.txt
```
4. Create Credentials in your root directory:
- IMPORTANT: NEVER commit the credentials.py file to version control (e.g., Git). It contains sensitive information.

```python
# credentials.py

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
```

`SECRET_KEY`: Replace the placeholder SECRET_KEY = '' with a strong, unique secret key for your Django project. You can generate one using:

`DATABASE`: Replace the placeholder with your actual database settings (e.g., PostgreSQL).

5. Run Migrations:
```bash
python manage.py migrate
```

6. Create Superuser:
```bash
python manage.py createsuperuser
```

7. Run Server:
```bash
python manage.py runserver
# or
.\run_dev.bat
```

### Working with Tailwind & HTMX

This project is already configured to use Tailwind and HTMX. It uses the popular third-party packages 'Django-Tailwind' and 'Django-HTMX' to integrate these technologies into the project.

```python
# settings.py
INSTALLED_APPS = [
    ...
    "django_htmx",
    'tailwind',
    'theme',
    ...
]
```

Base.html, which is the base template for all pages, includes the following lines:

```html
{% load static tailwind_tags django_htmx %}
<!DOCTYPE html>
<html lang="en">
    <head>
        {% tailwind_css %}
        <!-- Bootstrap Icons -->
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css" />
        <meta charset="UTF-8" />
        <title>
            {% block title %}{{ title }}{% endblock %}
        </title>
        <script src="{% static 'BaseApp/htmx.min.js' %}" defer></script>
        {% django_htmx_script %}
    </head>
```

The `{% tailwind_css %}` tag is used to include the Tailwind CSS stylesheet in the HTML document.

The `{% django_htmx_script %}` tag is used to include the HTMX script in the HTML document.

# Javascript Modules
## HOW TO USE BUTTON_HANDLERS.mjs
### ToggledButtonGroup

The ToggledButtonGroup class allows you to create interactive button groups where only one button can be active at a time. Clicking a button toggles its active state. You can customize the appearance of active buttons, choose the initially active button, and easily manage multiple button groups on your page.

#### Basic Usage

1. HTML Structure:

```html
<div id="myButtonGroup-button-group"> 
    <button>Button 1</button>
    <button>Button 2</button>
    <button>Button 3</button>
</div>
```
- Create a div container with an ID ending in "-button-group".
- Place your buttons inside this container.

`myButtonGroup`: The ID of the button group container.

2. Data Attributes:

```html
<div id="myButtonGroup-button-group"
     data-active-class="bg-blue-500 text-white"
     data-initial-active="2">
</div>

```
`data-active-class`: Specifies the CSS class(es) to apply to the active button. You can include multiple classes separated by spaces (e.g., bg-blue-500 text-white).

`data-initial-active`: Determines which button should be active when the page loads. It can be:
    - "first": Activates the first button.
    - "last": Activates the last button.
    - "none": No button is active initially.
    - "random": A random button is activated.
    - 1, 2, 3, etc.: Activates the button at the specified index (1-based).

3. JavaScript Initialization:

```javascript
import { ToggledButtonGroup } from "{% static 'BaseApp/button_handlers.mjs' %}";ToggledButtonGroup.initAll(); // Initializes all button groups on the page
```

- If you want to initialize only specific groups, you can pass a filter to `initAll()`:

```javascript
ToggledButtonGroup.initAll("myButtonGroup"); // Initializes only the group with ID "myButtonGroup-button-group"
```
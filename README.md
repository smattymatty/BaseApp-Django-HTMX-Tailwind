# Base Django App [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A customizable Django foundation with Tailwind CSS, HTMX, Loguru logging, and streamlined user management. Includes ready-to-use JavaScript modules for enhanced frontend interactivity.

This project is a work in progress, but feel free to use it and provide feedback! Contributions are welcome. 


## Features

* **Frontend Technologies:**
    * Tailwind CSS: A utility-first CSS framework for building modern designs.
    * HTMX:  A library for adding rich interactions without the need for full-page reloads.
* **Backend Enhancements:**
    * Loguru: A powerful logging library for structured, efficient logging.
    * Custom User Model:  Provides more flexibility than Django's built-in user model.
* **JavaScript Modules:** Ready-to-use components for adding interactive features to your templates (e.g., toggle button groups, modal handlers).

## Installation and Setup

1. Clone the repository: `git clone https://github.com/smattymatty/Base-Django-HTMX-Tailwind`
2. Change into the project directory: `cd Base-Django-HTMX-Tailwind`
3. Create/activate a virtual environment and install dependencies:
```bash
python -m venv venv  
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate  # Windows (Note: Use `.\` instead of `source`)
pip install -r requirements.txt
```
4. Create Credentials in your project's root:
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
.\run_dev.bat # Windows
run_dev.sh # Linux/macOS
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

`base.html`, which all pages inherit from, includes the following lines:

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

Run the command:
```bash
./tailwind_run.bat # Windows
./tailwind_run.sh # Linux/macOS
```
To start the Tailwind CSS development server provided by the 'Django-Tailwind' package.

# JavaScript Modules for Enhanced Interactivity
This project includes JavaScript modules to add interactive features to your Django templates.

Check the console for warnings and errors that should guide you through the process in case you are stuck.

## button_handlers.mjs
Button handlers are a set of classes that allow you to create interactive button groups.
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
"first": Activates the first button.
"last": Activates the last button.
"none": No button is active initially.
"random": A random button is activated.
1, 2, 3, etc.: Activates the button at the specified index (1-based).

3. JavaScript Initialization:

```javascript
import { ToggledButtonGroup } from "{% static 'BaseApp/button_handlers.mjs' %}";ToggledButtonGroup.initAll(); // Initializes all button groups on the page
```

- If you want to initialize only specific groups, you can pass a filter to `initAll()`:

```javascript
ToggledButtonGroup.initAll("myButtonGroup"); // Initializes only the group with ID "myButtonGroup-button-group"
```
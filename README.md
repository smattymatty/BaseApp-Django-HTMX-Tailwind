# BaseApp-Django-HTMX-Tailwind [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A customizable Django foundation with Tailwind CSS, HTMX, Loguru logging, and streamlined user management. Includes ready-to-use JavaScript modules for enhanced frontend interactivity.

This project is a work in progress, but feel free to use it and provide feedback! Contributions are welcome. 

There is a lot to re-do, and a lot of docs to write, especially for navigation and user management. I'm working on it.

## Features

* **Frontend Technologies:**
    * Tailwind CSS: A utility-first CSS framework for building modern designs.
    * HTMX:  A library for adding rich interactions without the need for full-page reloads.
* **Backend Enhancements:**
    * Loguru: A powerful logging library for structured, efficient logging.
    * Custom User Model:  Provides more flexibility than Django's built-in user model.
* **JavaScript Modules:** Ready-to-use components for adding interactive features to your templates (e.g., toggle button groups, modal handlers).

## Installation and Setup

1. **Clone the repository**: `git clone https://github.com/smattymatty/Base-Django-HTMX-Tailwind`
2. **Change into the project directory**: `cd Base-Django-HTMX-Tailwind`
3. **Create/activate a virtual environment and install dependencies**:
```bash
python -m venv venv  
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate  # Windows (Note: Use `.\` instead of `source`)
pip install -r requirements.txt
```
4. **Create Credentials in your project's root**:
- IMPORTANT: NEVER commit the credentials.py file to version control (e.g., Git). It contains sensitive information.
- This project includes a sample credentials_example.py file. Rename it to credentials.py and replace the placeholders with your actual credentials.

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

- `SECRET_KEY`: Replace the placeholder SECRET_KEY = '' with a strong, unique secret key for your Django project. You can generate one using: `python -c "import secrets; print(secrets.token_urlsafe(50))"`
- `DATABASE`: Replace the placeholder with your actual database settings (e.g., PostgreSQL), or use the sample SQLite configuration for initial setup and testing.

5. **Run Migrations**:
```bash
python manage.py migrate
```

6. **Create Superuser**:
```bash
python manage.py createsuperuser
```

7. **Run Server**:
```bash
python manage.py runserver
# or
.\run_dev.bat # Windows
run_dev.sh # Linux/macOS
```

### Working with Tailwind & HTMX

This project is already configured to use Tailwind and HTMX. It uses the popular third-party packages **[Django-Tailwind](https://github.com/timonweb/django-tailwind)** and **[Django-HTMX](https://github.com/adamchainz/django-htmx)** to integrate these technologies into the project.

```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_htmx',
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

### Working with Loguru

This project utilizes Loguru, a powerful and flexible logging library for Python, to provide a structured and efficient logging system.

#### Key Benefits

- **Simple Setup**: Loguru's configuration is intuitive and concise.
- **Customization**: You can easily customize log formats, levels, and destinations.
- **Automatic File Rotation**: Log files are automatically rotated based on size or time, preventing them from growing too large.
- **Filtering**: You can filter logs based on specific criteria, such as log level, module name, or any custom attribute.
- **Context Binding**: Loguru allows you to bind contextual information to your log records for better traceability.

#### Configuration

The main Loguru configuration is located in the `BaseApp/utils.py` file. It includes:

- `get_module_logger`: This function is used to create a logger instance for a specific module.
- `from .constants import LOG_FORMAT`: The log format includes the timestamp, log level, module name, and the log message. This lies in the `BaseApp/constants.py` file.
```python
#constants.py
LOG_FORMAT = "{time} -- {level} -- {function} -- line {line}\n\t {message}"
```

#### Usage

1. **Import the Logger**:
```python
from BaseApp.utils import get_module_logger
```
2. **Get the logger instance**:
```python
logger = get_module_logger("my_module", __file__)
```
This line creates a logger instance bound to the "my_module" module and the file where the logger is being used.
3. **Log Messages**:
Use the standard Loguru logging methods:
```python
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```
4. **Customizing Log Levels**: 
You can adjust the minimum log level in get_module_logger to control which messages are logged.

#### Example: Logging in `CustomUserManager`
```python
# In your managers.py file:
from BaseApp.utils import get_module_logger
module_logger = get_module_logger("managers", __file__)

# ... later in your code ...
module_logger.debug(f"Creating user with username: {username} and email: {email}")
```
In this example, module_logger logs a debug message when a new user is being created. This helps you track user creation activities.

# Modules for Enhanced Frontend Interactivity

This project provides a collection of JavaScript modules designed to supercharge your Django templates with interactive features,
**without the need for any custom JavaScript code**.
Simply load the corresponding template tags, add some data attributes to your HTML elements, and let the magic happen!

- **Seamless Django Integration:** The modules are built to work effortlessly with Django's templating system.
- **Zero JavaScript Overhead:** You don't need to write or manage any custom JavaScript code.
- **Enhanced User Experience:** Add rich interactivity to your web pages with minimal effort.
- **Customizable:** Tailor the modules to your specific design and functionality needs using intuitive data attributes.

## ToggledButtonGroup
[button_example_1]](BaseApp/ui_elements/partials/button_example_1.html) for an example.
![Gif of buttons changing](https://i.imgur.com/lfe5AWF.gif)
The `ToggledButtonGroup` class allows you to create interactive button groups where only one button can be active at a time. Clicking a button toggles its active state. You can customize the appearance of active buttons, choose the initially active button, and easily manage multiple button groups on your page.

### Basic Usage

1. **HTML Structure**:

```html
{% load button_group_tags %}
<form id="myButtonGroup-toggled-button-group"> 
    <button>Button 1</button>
    <button>Button 2</button>
    <button>Button 3</button>
</form>
```

- load the `button_group_tags` template tag

- Create a container with an ID ending in "-toggled-button-group".
    - The container does not have to be a form, but it is recommended for `hx-post` integration.
- Place your buttons inside this container.

`myButtonGroup`: The ID of the button group container.

2. **Customize with Data Attributes (Optional)**:

```html
<form id="myButtonGroup-toggled-button-group"
     data-active-class="bg-blue-500 text-white"
     data-initial-active="2">
</form>

```
`data-active-class`: Specifies the CSS class(es) to apply to the active button. You can include multiple classes separated by spaces (e.g., bg-blue-500 text-white).

`data-initial-active`: Determines which button should be active when the page loads. It can be:
- "none": No button is active initially. (DEFAULT)
- "first": Activates the first button.
- "last": Activates the last button.
- "random": A random button is activated.
- "0", "1", "2", etc.: Activates the button at the specified index.

3. **Initialize with the Django Template Tag**:

```html
<div id="myButtonGroup-toggled-button-group">
    ...
</div>
{% init_button_groups "myButtonGroup" %} 
```

- You can initialize all button groups on the page with `{% init_button_groups %}` or you can initialize a specific button groups with `{% init_button_groups "name1" "name2" "name3" %}`.

### HTMX Integration (GET)
The ToggledButtonGroup class seamlessly integrates with HTMX. When your buttons include the hx-get attribute, HTMX will automatically handle fetching and updating the content based on the initially active button (as specified by the data-initial-active attribute).

- **HTMX Attributes**: Add standard HTMX attributes to the buttons within your button group container:
    - `hx-get`: Specifies the URL to fetch when the button is clicked.
    - `hx-target`: Specifies the element on the page to update with the content returned by the HTMX request.
    - `hx-swap`: Specifies how the returned content should be swapped into the target element (e.g., "innerHTML", "outerHTML", "beforeend").
**Example:**
```html
<div id="myButtonGroup-toggled-button-group"
     data-initial-active="random">
    <button hx-get="/get-content-1" 
            hx-target="#contentArea"
            hx-trigger="mousedown">
            Button 1
    </button>
    <button hx-get="/get-content-2" 
            hx-target="#contentArea"
            hx-trigger="mousedown">
            Button 2
    </button>
    <button hx-get="/get-content-3" 
            hx-target="#contentArea"
            hx-trigger="mousedown">
            Button 3
    </button>
</div>

<div id="contentArea"></div>
```
In this example, the initial active button is randomly selected, and will automatically perform the first HTMX request when the page loads.

### HTMX Integration (POST)

The ToggledButtonGroup class automates sending POST requests using HTMX when a button in the group is initially activated.

1. Include Django's CSRF Token:
- To ensure the security of your POST requests, include Django's CSRF token in your form element. Django provides a convenient template tag for this:
```html
<form id="myButtonGroup-toggled-button-group">
    {% csrf_token %}
    ...
</form>
```
2. Add buttons with the `hx-post` attribute to your button group:
```html
<button hx-post="{% url 'BaseApp:display_number' %}"
        hx-trigger="click"
        hx-target="#result-container"
        hx-swap="innerHTML"
        name="number"
        value="0"
        class="...">
            Button
</button>
<button hx-post="{% url 'BaseApp:display_number' %}"
        hx-trigger="click"
        hx-target="#result-container"
        hx-swap="innerHTML"
        name="number"
        value="1"
        class="...">
    Button
</button>
```

`hx-post`: This attribute indicates that an HTTP POST request should be sent when the button is clicked. You'll specify the URL of your Django view function that handles the request.
`name`: This attribute specifies the name of the form field that will be submitted with the POST request.
`value`: This attribute specifies the value of the form field that will be submitted with the POST request.

3. Create a Django view function that handles the POST request:
```python
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_POST

@require_POST
def display_number(request):
    # Retrieve the button value from the POST data
    number = request.POST.get('number')
    # Render the template with the number
    template = loader.get_template('BaseApp/tests/number_display.html')
    context = {'number': number}
    return HttpResponse(template.render(context, request))
```

**Full Example:**
```html
{% load button_group_tags %}
<div id="myButtonGroup-toggled-button-group" 
    data-active-class="bg-blue-500 text-white" data-initial-active="random">
    <button hx-post="{% url 'BaseApp:display_number' %}"
            hx-trigger="mousedown"
            hx-target="#result-container"
            hx-swap="innerHTML"
            name="number"
            value="0"
            class="...">
            Button 0
    </button>
    <button hx-post="{% url 'BaseApp:display_number' %}"
            hx-trigger="mousedown"
            hx-target="#result-container"
            hx-swap="innerHTML"
            name="number"
            value="1"
            class="...">
            Button 1
    </button>
    <button hx-post="{% url 'BaseApp:display_number' %}"
            hx-trigger="mousedown"
            hx-target="#result-container"
            hx-swap="innerHTML"
            name="number"
            value="2"
            class="...">
            Button 2
    </button>
</div>

<div id="result-container"></div>

{% init_button_groups "myButtonGroup" %}
```
How it Works

1. When a button is clicked, HTMX intercepts the event.
2. HTMX constructs a POST request to the specified URL ({% url 'BaseApp:display_number' %}).
3. The request includes the data from the button, which can include the csrf token if the button is in the form or if the button has the hx-include attribute.
4. Your Django view function (display_number) processes the POST data and returns a response.
5. HTMX updates the specified target element (result-container) with the content returned from the server.
# Django REST Api

This project is a RESTful API that provides user authentication and authorization for Django applications. It allows users to register, login, logout, update, and delete their accounts using JSON web tokens (JWT). It also supports password reset and email verification features.

This project was created to demonstrate how to use Django REST framework and django-rest-auth to build a secure and scalable API for web and mobile applications.

## Project structure

```bash
Django-Rest-Api/
├── .envs/ # Contains environment variables files for different environments
│   └── .env.example
├── scripts/ # Contains custom scripts or utilities for Django project
│   ├── production_data.py # The script to create data for production (e.g SECRET_KEY, ...)
│   └── dockerized-drest-run.sh # The script to run as entrypoint for docker container starting
├── dj_rest_api/  # Contains source files for Django project
│   ├── apps/ # Contains apps for Django project
│   │   ├── accounts/
│   │   ├── authentication/
│   │   └── core/
│   │
│   ├── config/ # Contains configuration files for Django project
│   │   ├── settings/ # Contains settings modules for different environments
│   │   │   ├── components/ # Contains common settings components for all environments
│   │   │   │   ├── base.py
│   │   │   │   ├── custom.py
│   │   │   │   ├── database.py
│   │   │   │   ├── email.py
│   │   │   │   ├── pytest.py
│   │   │   │   └── third_party.py
│   │   │   ├── environments/ # Contains specific settings modules for each environment
│   │   │   │   ├── development.py
│   │   │   │   ├── production.py
│   │   │   │   └── test.py
│   │   │   ├── __init__.py # Contains using of split_settings module for multiple settings
│   │   │   └── envvars.py # Contains mechanism for overriding settings configuration from .env file
│   │   ├── urls.py
│   │   ├── celery.py # Contains specific settings for celery configurations
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── test/ # Contains tests for Django project
│   └── manage.py
│
├── Makefile # The make utility for Django project
├── poetry.lock
├── pyproject.toml
├── .dockerignore
├── docker-compose.dev.yml # The Docker Compose file for local development
├── docker-compose.yml # The Docker Compose file for production deployment
├── Dockerfile
└── README.md
```

## Project Setup

### Prerequisite Installation

Before you begin, ensure you have the following prerequisites installed:

- **Python**:
  You should have Python 3 installed. If not, download the latest version [here](https://www.python.org/downloads/).

- **Make**:
  - For Windows systems (in PowerShell):

    ```bash
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```

  - For Linux systems:

    ```bash
    sudo apt install make
    ```

- **Poetry**:
  - For Windows systems (in PowerShell):

    ```bash
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```

    To add Poetry to your system environment:

    ```bash
    setx path "%path%;C:\Users\{%user_name%}\AppData\Roaming\Python\Scripts"
    ```

  - For Linux systems:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    To add Poetry to your environment path:
    - Open the file:

    ```bash
    nano ~/.bashrc
    ```

    - Add the following command to the file to export Poetry to environment variables:

    ```bash
    export PATH="/home/sammy/.local/bin:$PATH"
    ```

    - Apply the changes:

    ```bash
    source ~/.bashrc
    ```

### Building

1. Clone the repository:

```bash
 git clone https://github.com/Nicola-Ibrahim/Django-Rest-Api.git

```

2. Navigate to the project directory:

  ```bash
    cd Django-Rest-Api
  ```

3. Edit the poetry configuration to create virtualenv in the root directory

  ```bash
    poetry config virtualenvs.in-project true
  ```

4. Install all dependencies (including development dependencies) using Poetry:

  ```bash
    make install
  ```

5. Activate the created virtual environment:

- For Windows:

  ```bash
    .venv\Scripts\activate
  ```

- For Linux:

  ```bash
    source .venv/bin/activate
  ```

4. Run migrations and install pre-commit:

  ```bash
    make update
  ```

## Running

To start the server, use the following command:

```bash
  make run-server
```

### Installing and Running Redis

- Windows:
  To install Redis on a Windows system, follow these steps:

  1. Download Redis for Windows from Microsoft Archive.
  2. Extract the downloaded zip file to a directory of your choice.
  3. Open a Command Prompt and navigate to the Redis directory.
  4. Run the following command to start the Redis server:

   ```bash
   redis-server.exe
   ```

- Linux:
  To install Redis on a Linux system, follow these steps:

  1. Open a terminal.
  2. Update the package list to ensure you have the latest information on available packages:

   ```bash
    sudo apt update
   ```

  3. Install Redis by running:

   ```bash
    sudo apt install redis-server
   ```

  4. Start the Redis server:

    ```bash
    sudo systemctl start redis-server
   ```

### Running Celery

After setting up Redis, you can run Celery to perform background tasks in your Django project. Make sure you are in your project directory (Django-Rest-Api) and your virtual environment is activated.

- Windows:
  To run Celery on Windows, use the following command:

  ```bash
  poetry run celery -A dj_rest_api worker --loglevel=info --pool=solo
  ```

- Linux:
  To run Celery on Linux, use the following command:

  ```bash
  poetry run celery -A dj_rest_api worker --loglevel=info
  ```

# 🐍 Django REST Api 🌐

[![Python](https://img.shields.io/badge/python-3.12-3670A0?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![RESTful](https://img.shields.io/badge/RESTful-0096D8?style=flat)](https://en.wikipedia.org/wiki/Representational_state_transfer)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

This project is a RESTful API that provides user authentication and authorization for Django applications. It allows users to register, login, logout, update, and delete their accounts using JSON web tokens (JWT). It also supports password reset and email verification features.

This project was created to demonstrate how to use Django REST framework and django-rest-auth to build a secure and scalable API for web and mobile applications.

## Table of contents

- [🐍 Django REST Api 🌐](#-django-rest-api-)
  - [Table of contents](#table-of-contents)
- [Technologies](#technologies)
  - [Project structure](#project-structure)
  - [Project Setup](#project-setup)
    - [Prerequisite Installation](#prerequisite-installation)
    - [Building](#building)
  - [Running](#running)
    - [Installing and Running Redis](#installing-and-running-redis)
  - [Running dockerized](#running-dockerized)

# Technologies

The Django REST API project utilizes the following technologies:

- **Python**: The primary programming language used for backend development.
- **Django**: A high-level Python web framework for rapid development and clean, pragmatic design.
- **Django REST Framework (DRF)**: A powerful and flexible toolkit for building Web APIs in Django.
- **django-rest-auth**: A Django app for handling user authentication and registration.
- **JSON Web Tokens (JWT)**: Used for secure authentication and authorization.
- **Poetry**: Dependency management tool for Python projects.
- **Make**: Utility for automating tasks and managing project workflow.
- **Redis**: In-memory data structure store used as a message broker for Celery.
- **Celery**: Distributed task queue for background job processing.
- **Docker**: Containerization platform used for creating reproducible and portable development environments.

## Project structure

```bash
Django-Rest-Api/
├── dj_rest_api/  # Contains source files for Django project
│   ├── apps/  # Contains Django apps
│   │   ├── accounts/  # App for user accounts functionality
│   │   └── authentication/  # App for authentication functionality
│   │
│   ├── config/  # Contains configuration files for Django project
│   │   ├── settings/  # Contains settings modules for different environments
│   │   │   ├── components/  # Contains common settings components for all environments
│   │   │   │   ├── base.py  # Base settings shared across all environments
│   │   │   │   ├── custom.py  # Custom settings overrides
│   │   │   │   ├── database.py  # Database settings
│   │   │   │   ├── email.py  # Email settings
│   │   │   │   ├── i18n.py  # i18n settings
│   │   │   │   └── third_party.py  # Third-party app settings
│   │   │   ├── environments/  # Specific settings modules for each environment
│   │   │   │   ├── development.py  # Development environment settings
│   │   │   │   ├── production.py  # Production environment settings
│   │   │   │   └── test.py  # Testing environment settings
│   │   │   ├── __init__.py  # Initialization file for settings
│   │   │   └── envvars.py  # Mechanism for overriding settings configuration from .env file
│   │   ├── urls.py  # Django project URL configuration
│   │   ├── celery.py  # Specific settings for Celery configurations
│   │   ├── asgi.py  # ASGI application entry point
│   │   └── wsgi.py  # WSGI application entry point
│   │
│   ├── core/  # Contains core files and modules
│   ├── locale/  # Contains translations files for localization
│   ├── tests/  # Contains tests for Django project
│   ├── conftest.py  # Configuration file for pytest
│   └── manage.py  # Django project management script
│
├── .envs/  # Contains environment variables files for different environments
│   └── .env.example  # Example environment variables file
├── scripts/  # Contains custom scripts or utilities for Django project
│   ├── production_data.py  # Script to create data for production environment (e.g., SECRET_KEY)
│   └── dockerized-drest-run.sh  # Script to run as entrypoint for Docker container starting
├── logging/  # Directory for log files
├── Makefile  # Make utility file for managing project tasks
├── poetry.lock  # Lock file generated by Poetry
├── pyproject.toml  # Poetry configuration file
├── .dockerignore  # List of files and directories to ignore in Docker builds
├── docker-compose.dev.yml  # Docker Compose file for local development environment
├── docker-compose.yml  # Docker Compose file for production deployment
├── Dockerfile  # Dockerfile for building Docker images
└── README.md  # Project README file

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

## Running dockerized

To start the server, use the following command:

```bash
  make dev-docker
```

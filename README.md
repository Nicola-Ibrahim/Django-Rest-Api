# Django authentication RestAPI

## Project structure

```bash
django-auth/
├── .envs/ # Contains environment variables files for different environments
│   └── .env.example # An example of environment variables file
├── config/ # Contains configuration files for Django project
│   ├── settings/ # Contains settings modules for different environments
│   │   ├── components/ # Contains common settings components for all environments
│   │   ├── environments/ # Contains specific settings modules for each environment (e.g. base.py, development.py, production.py)
│   │   ├── __init__.py # Contains using of split_settings module for multiple settings
│   │   └── envvars.py # Contains mechanism for overriding settings configuration from .env file
│   ├── urls.py # The URL configuration file for Django project
│   ├── asgi.py # The ASGI application file for Django project
│   └── wsgi.py # The WSGI application file for Django project
│
├── scripts/ # Contains custom scripts or utilities for Django project
│   ├── production_data.py # The script to create data for production (e.g SECRET_KEY, ...)
│   └── dockerized-dauth-run.sh # The script to run as entrypoint for docker container starting
├── src/  # Contains source files for Django project
│   ├── apps/ # Contains apps for Django project
│   └── tests/ # Contains tests for Django project
│
├── Makefile # The make utility for Django project
├── manage.py # The command-line utility for Django project
├── poetry.lock # The lock file generated by poetry package manager
├── pyproject.toml # The configuration file for poetry package manager
├── .dockerignore # The file that tells Docker what files to ignore when building images
├── docker-compose.yml # The Docker Compose file for local development
├── docker-compose.prod.yml # The Docker Compose file for production deployment
├── Dockerfile # The file that defines how to build a Docker image for Django service
└── README.md # The documentation file for Django project
```

## Project setup

Project setup instruction here.

- Cloning the repo:

  ```bash
    git clone https://github.com/Nicola-Ibrahim/django-auth.git
  ```

- Go to the project directory

  ```bash
    cd django-auth
  ```

- For windows system:

  - install make in powershell:

    ```bash

    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```

  - Install poetry

    In Powershell: install poetry for package management using

    ```bash
      (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```

  - Add poetry to system environment

    ```bash
      setx path "%path%;C:\Users\{%user_name%}\AppData\Roaming\Python\Scripts"
    ```

- For linux system:

  - install make in terminal:

    ```bash
      sudo apt install make
    ```

  - Install poetry

    In terminal: install poetry for package management using

    ```bash
      curl -sSL https://install.python-poetry.org | python3 -
    ```

    Add to poetry to environment path

    open the file:

    ```bash
      nano ~/.bashrc
    ```

    Add the following command to file to export poetry to env variables:

    ```bash
      export PATH="/home/sammy/.local/bin:$PATH"
    ```

    Apply changes

    ```bash
      source ~/.bashrc
    ```

- Edit the poetry configuration to create virtualenv in the root directory

  ```bash
    poetry config virtualenvs.in-project true
  ```

- Install all dependencies (++ development) using poetry

  ```bash
    poetry install
  ```

- Activate the created environment

  ```bash
    .venv\Scripts\activate
  ```

- Custom dev settings:

  If want to create custom settings.dev.py, create local directory in the root

  ```bash
    mkdir local
  ```

  Copy settings.dev.py to local directory for further modification

  ```bash
    copy src\config\settings\environments\settings.dev.py.template .\local\settings.dev.py
  ```

## Start the server

- with make

```bash
  make run-server
```

- with poetry

```bash
  poetry run python src\manage.py runserver 127.0.0.1:8000
```

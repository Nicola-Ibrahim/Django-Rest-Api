# Django authentication RestAPI

## Project structure

```bash
django-auth/
├── .envs/ # Contains environment variables files for different environments
│   └── .env.example
├── scripts/ # Contains custom scripts or utilities for Django project
│   ├── production_data.py # The script to create data for production (e.g SECRET_KEY, ...)
│   └── dockerized-drest-run.sh # The script to run as entrypoint for docker container starting
├── dj-rest-api/  # Contains source files for Django project
│   ├── apps/ # Contains apps for Django project
│   │   ├── accounts/
│   │   ├── authentication/
│   │   └── core/
│   ├── test/ # Contains tests for Django project
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
│   │   ├── asgi.py
│   │   └── wsgi.py
│
├── Makefile # The make utility for Django project
├── manage.py
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
 git clone https://github.com/Nicola-Ibrahim/django-auth.git

```

2. Navigate to the project directory:

  ```bash
    cd django-auth
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

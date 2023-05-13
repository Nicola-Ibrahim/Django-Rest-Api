# Medical equipment store website

### Django-Rest framework

#### The project is an online medical equipment store for selling and buying medical equipment.

#### The website handles all necessary processes for buying and displaying products.

#### For who:

- Medical warehouses that want to sell their products.
- Doctors that want to buy products.
- Delivery workers that want work as middler between warehouses and doctors.

#### The main entities are:

- Admins.
- Doctors.
- warehouses.
- staff:
  - Accountant (For various external users).
  - Statistician.

# Project setup

Project setup instruction here.

Clone the project

```bash
  git clone https://github.com/Nicola-Ibrahim/Medical-Equipment-Store.git
```

Go to the project directory

```bash
  cd Medical-Equipment-Store
```

In Powershell: install poetry for package management using

```bash
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Add poetry to system environment

```bash
  setx path "%path%;C:\Users\{%user_name%}\AppData\Roaming\Python\Scripts"
```

Change the virtualenv directory to current directory

```bash
  poetry config virtualenvs.in-project true
```

Install dependencies using poetry

```bash
  poetry install
```

Activate the created environment

```bash
  .venv\Scripts\activate
```

Create local directory to create custom settings

```bash
  mkdir local
```

Copy settings.dev.py to local directory for further modification

```bash
  copy core\home\settings\templates\settings.dev.py .\local\settings.dev.py
```

Start the server

- with make

```bash
  make run-server
```

- with poetry

```bash
  poetry run python -m core.manage runserver 127.0.0.1:8000
```

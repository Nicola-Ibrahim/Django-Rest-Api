######################
# builder-dev  STAGE #
######################
# it is responsible for installing poetry, createing env, installing project dependencies

# Use python:3.11-buster as the builder image
FROM python:3.11-buster AS builder-dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.5.1

# Set the PYTHONPATH environment variable to the current directory
ENV PYTHONPATH .

# Install dependencies
RUN set -xe \
    && apt-get update \
    # Install build-essential for compiling C extensions 'libpq-dev'
    && apt-get install -y --no-install-recommends build-essential netcat curl\
    && pip install virtualenvwrapper "poetry==$POETRY_VERSION" \
    # Clean up the cache and temporary files
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

COPY ["poetry.lock", "pyproject.toml", "./"]

# Create a virtual environment in the backend folder with poetry
RUN poetry config virtualenvs.in-project true --local \
    && poetry install $(test "$DJANGO_ENV" == production && echo "--without dev test") --no-root --no-interaction --no-ansi

COPY . /backend


###############
# FINAL STAGE #
###############
# it is responsible for copying the source code and the wheels
# from the builder stage and installing them with pip

FROM python:3.11-buster

# Copy source code from builder stage
COPY --from=builder-dev /backend /backend

WORKDIR /backend

# # Create a new user "appuser" with user id 5678 without home directory
# RUN useradd -u 5678 -M --no-create-home --shell /bin/bash appuser \
#     && chown -R appuser /backend

# # Switch to "appuser" for subsequent commands
# USER appuser


# Make the dockerized-dauth-run script executable
RUN chmod +x /backend/scripts/dockerized-dauth-run.sh


# Run the dockerized-dauth-run script as the default command when starting the container
ENTRYPOINT ["/backend/scripts/dockerized-dauth-run.sh"]

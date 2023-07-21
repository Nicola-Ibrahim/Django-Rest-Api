# For more information, please refer to https://aka.ms/vscode-docker-python
# Use python:3.11-slim as the base image
FROM python:3.11-slim

# Expose port 8000 for the web server
EXPOSE 8000

# Set the working directory in the container to /backend
WORKDIR /backend

# Copy the current directory contents into the container at /backend
COPY . /backend

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set the PYTHONPATH environment variable to the current directory
ENV PYTHONPATH .

# # Install poetry and dependcies
# RUN curl -sSL https://install.python-poetry.org | python3 -
# RUN poetry install

# Install dependencies
RUN set -xe \
    # Update the package list
    # && apt-get update \
    # Install build-essential for compiling C extensions
    # && apt-get install -y --no-install-recommends build-essential \
    # Install virtualenvwrapper and poetry with pip
    && pip install virtualenvwrapper poetry==1.4.2 \
    # Clean up the cache and temporary files
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN poetry install --no-root

# Disable virtualenv creation by poetry
# RUN poetry config virtualenvs.create false

# Expose port 8000 for the web server
EXPOSE 8000

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]


# Set up the entrypoint script for running commands before starting the web server
COPY scripts/entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod a+x /entrypoint.sh

# Run the entrypoint script as the default command when starting the container
ENTRYPOINT ["/entrypoint.sh"]

# Pull base image
FROM python:3.11-slim

# Set the working directory to /code
WORKDIR /code

# Update and install all in the container and clean up apt cache to reduce image size
RUN apt-get update && \
    apt-get install -y \\
    xvfb \\
    libx11-6 \\
    libxext6 \\
    xauth \\
    && rm -rf /var/lib/apt/lists/*

# Install and update pip and pipenv and install all dependency
RUN pip install --upgrade pip pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --deploy --system

# Copy the current directory content into the container at /code
ADD . /code
# Set enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
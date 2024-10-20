# Pull base image
FROM python:3

# Set the working directory to /code
WORKDIR /code

# Copy the Pipfile and Pipfile.lock first to leverage Docker cache
COPY Pipfile Pipfile.lock /code/

# Install pipenv and dependencies
RUN pip install --upgrade pip
RUN pip install pipenv

# Install the dependencies in the system (not in a virtualenv, since you're using --system)
RUN pipenv install --deploy --system --skip-lock --dev

# Copy the rest of the application code
COPY . /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run your application (replace 'your_app.py' with your entry point file)
CMD ["python", "."]

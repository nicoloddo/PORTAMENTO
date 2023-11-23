# Build from image of Python version used in the development
FROM python:3.9.13-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# This sets the PYTHONPATH environment variable to include our working directory.
# It ensures that Python will include the directories inside '/usr/src/app' when searching for modules to import.
# This is crucial for correctly resolving our project's internal module imports in a Dockerized environment.
ENV PYTHONPATH /usr/src/app
# This sets another environment variable pointing at the tests folder.
# Doing this allows us to save the tests results in a fixed folder even if running the tests from any subpath of the container.
ENV TESTS_PATH /usr/src/app/test

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Run the application when the container launches
# CMD ["python", "cloud_services/aws_lambda_handler/playlist_processor_handler.py"] # When deploying on Lambda

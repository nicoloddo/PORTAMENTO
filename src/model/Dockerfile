# Define custom function directory
ARG FUNCTION_DIR="/usr/src/app"

# First stage: Build image
FROM python:3.11.10-slim as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Set the working directory in the container
WORKDIR ${FUNCTION_DIR}

# Copy the current directory contents into the container
COPY . ${FUNCTION_DIR}

# Define a build-time argument
ARG REQUIREMENTS_FILE=requirements.txt

# Copy the entire requirements folder
COPY requirements/ ./requirements/

# Install dependencies using the specified requirements file
RUN pip install --no-cache-dir --target ${FUNCTION_DIR} -r ./requirements/${REQUIREMENTS_FILE} \
    && pip install --no-cache-dir --target ${FUNCTION_DIR} awslambdaric

# Set environment variables
ENV PYTHONPATH ${FUNCTION_DIR}
ENV PYTHON_TESTS_PATH ${FUNCTION_DIR}/test/python

# Second stage: Slim version of the base Python image
FROM python:3.11.10-slim

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies from the build-image
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set runtime interface client as the entry point
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

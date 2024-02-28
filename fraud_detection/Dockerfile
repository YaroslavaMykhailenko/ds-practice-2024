# Use an official Python runtime as the base image
# FROM python:3.10
FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory in the container
# Both the utils and src folders will be mounted as volumes, please see docker-compose.yaml
WORKDIR /app

COPY . .
RUN cd utils/pb && pip install .
WORKDIR /app

# Copy the requirements file to the working directory
COPY ./fraud_detection/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Install reloadium for hot reloading
# This allows us to make changes to the code without having to rebuild the container
RUN pip install reloadium

# Set the command to run the application
CMD reloadium run "fraud_detection/src/app.py"
# CMD ["python", "fraud_detection/src/app.py"]
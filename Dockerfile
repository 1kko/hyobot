# docker file launches the serve:app command with environment of .env

# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip

# Copy the current directory contents into the container at /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Entry point
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

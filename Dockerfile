# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependency list and install them
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of the application's code into the container
COPY . /app/
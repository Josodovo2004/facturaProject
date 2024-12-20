# Use official Python image as a base
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "facturaProject.wsgi:application"]

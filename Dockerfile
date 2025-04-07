# Use the official Python 3.11 slim image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . /app/

# Set environment variables
ENV DJANGO_SECRET_KEY=your-secret-key
ENV DEBUG=False
ENV ALLOWED_HOSTS=your-app-name.up.railway.app

# Collect static files and apply migrations on container startup
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn backend.wsgi:application"]

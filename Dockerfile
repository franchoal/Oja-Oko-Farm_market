FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy all files to the container
COPY . /app/

# Set environment variables
ENV DJANGO_SECRET_KEY=your-secret-key
ENV DEBUG=False
ENV ALLOWED_HOSTS=your-app-name.up.railway.app

# Run migrations and collectstatic on startup
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn backend.wsgi:application"]

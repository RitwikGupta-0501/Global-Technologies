FROM python:3.14-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create media directory
RUN mkdir -p media

EXPOSE 8000

CMD ["gunicorn", "global_tech.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

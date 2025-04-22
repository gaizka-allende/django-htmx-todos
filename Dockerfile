FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt .
RUN pip install -r requirements.txt

# The actual source code will be mounted as a volume
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

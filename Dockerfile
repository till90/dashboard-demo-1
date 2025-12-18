FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Optional, aber oft hilfreich falls ein Paket mal aus Source gebaut werden muss
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# Cloud Run setzt PORT automatisch. Fallback 8080 für lokal.
CMD ["sh", "-c", "gunicorn app:server --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 8 --timeout 0 --access-logfile - --error-logfile -"]

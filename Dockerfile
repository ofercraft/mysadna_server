# ===============================
# 1. Base image
# ===============================
FROM python:3.11-slim

# Avoid Python writing .pyc files and using buffered stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ===============================
# 2. Work directory
# ===============================
WORKDIR /app

# ===============================
# 3. Install system dependencies
# ===============================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade certifi

# ===============================
# 4. Copy project files
# ===============================
COPY requirements.txt .

# ===============================
# 5. Install Python dependencies
# ===============================
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates

# Copy the rest of the application
COPY . .

# ===============================
# 6. Expose Cloud Run port
# ===============================
ENV PORT=8080
EXPOSE 8080

# ===============================
# 7. Run with Gunicorn (production WSGI server)
# ===============================
# app:app means "file app.py, object named app"
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 8 app:app

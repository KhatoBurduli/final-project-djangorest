# ----------------------------
# 1. Base image
# ----------------------------
FROM python:3.12-slim

# ----------------------------
# 2. Environment variables
# ----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------------
# 3. Work directory
# ----------------------------
WORKDIR /final-project-django-rest

# ----------------------------
# 4. Install system dependencies
# ----------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# 5. Install Python dependencies
# ----------------------------
COPY requirements.txt /final-project-django-rest/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------
# 6. Copy project files
# ----------------------------
COPY . /final-project-django-rest/

# ----------------------------
# 7. Collect static files
# ----------------------------
# RUN python manage.py collectstatic --noinput

# ----------------------------
# 8. Expose port
# ----------------------------
EXPOSE 8000

# ----------------------------
# 9. Run the Django app
# ----------------------------
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

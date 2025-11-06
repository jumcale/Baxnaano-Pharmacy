FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x /app/entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=pharmacy.settings \
    TZ=Africa/Mogadishu

CMD ["/app/entrypoint.sh", "gunicorn", "pharmacy.wsgi:application", "--bind", "0.0.0.0:8000"]
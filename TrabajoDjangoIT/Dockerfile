FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt manage.py /app/

COPY mi_primer_proyecto_django /app/mi_primer_proyecto_django

COPY blog /app/blog

RUN pip install --upgrade pip && pip install -r requirements.txt
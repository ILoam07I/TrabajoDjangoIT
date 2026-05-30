FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt manage.py /app/

COPY trabajo_it /app/trabajo_it

COPY beatemplate /app/beatemplate

RUN pip install --upgrade pip && pip install -r requirements.txt
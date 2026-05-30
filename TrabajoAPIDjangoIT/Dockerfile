FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt manage.py /app/

COPY api_trabajo_it /app/api_trabajo_it

COPY restemplate /app/restemplate

RUN pip install --upgrade pip && pip install -r requirements.txt
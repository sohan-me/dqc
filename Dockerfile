FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

RUN apk add --no-cache && pip install --upgrade pip

WORKDIR /quote_companion

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

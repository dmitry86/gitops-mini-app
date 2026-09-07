FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["sh", "-c", "python -c 'from app import init_db; init_db()' && gunicorn -b 0.0.0.0:8000 app:app"]

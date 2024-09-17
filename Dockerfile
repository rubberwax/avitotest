FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r backend/requirements.txt

EXPOSE 8080

CMD ["python", "backend/app.py"]
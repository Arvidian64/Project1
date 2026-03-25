FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY server.py server.py
COPY relational_database.py relational_database.py

EXPOSE 5000

CMD ["python3", "-u", "server.py"]
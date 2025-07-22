# Dockerfile
FROM python:3.10-slim
WORKDIR /app

COPY app/ /app/

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000 8501

CMD ["python", "main.py"]

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY run.py .

ENV PORT=3939

EXPOSE 3939

CMD ["python", "run.py"]

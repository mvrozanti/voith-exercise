FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app/voith_exercise
COPY voith_exercise /app/voith_exercise

WORKDIR /app/voith_exercise

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

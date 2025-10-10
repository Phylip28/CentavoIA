# Stage 1

FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Stage 2

FROM python:3.11-slim

WORKDIR /app

RUN useradd --create-home appuser

COPY --from=builder /app/wheels /wheels/

RUN pip install --no-cache /wheels/*

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
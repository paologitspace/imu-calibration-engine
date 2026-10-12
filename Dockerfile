FROM python:3.12-slim

LABEL maintainer="pablo"
LABEL description="IMU Calibration & Fusion Engine Microservice"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --shell /bin/bash appuser
USER appuser

COPY --chown=appuser:appuser main.py .
COPY --chown=appuser:appuser models/ ./models/
COPY --chown=appuser:appuser services/ ./services/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

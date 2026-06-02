FROM python:3.11-slim

LABEL maintainer="agulo.joshclarence@gmail.com"
LABEL description="Space Mission Telemetry Data Parser"
LABEL version="1.0.0"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY parse_data.py .
RUN mkdir -p /app/data && chmod +x parse_data.py

ENTRYPOINT ["python", "parse_data.py"]
CMD ["/app/data/missions.xml"]
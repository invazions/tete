FROM python:3.12.10-alpine3.21 AS builder

RUN apk add --no-cache \
    nmap \
    nmap-scripts \
    lua \
    libpcap \
    openssl \
    libssh2

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
#COPY main.py .
#COPY nmap_scanner.py .

# CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
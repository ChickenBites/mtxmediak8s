FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy operator code
COPY main.py .
COPY templates.py .
COPY utils.py .
COPY VERSION .

# Kopf entrypoint
CMD ["kopf", "run", "main.py"]

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# workdirectory
WORKDIR /app

# dependency
RUN pip install --no-cache-dir fastapi uvicorn llama-cpp-python huggingface-hub


COPY main.py index.html icon.png /app/

EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
FROM python:3.11-slim

WORKDIR /app

# Copy requirements.txt first to leverage Docker cache if dependencies don't change
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script
COPY baseApi.py .

# Run the Python script
CMD ["python", "baseApi.py"]
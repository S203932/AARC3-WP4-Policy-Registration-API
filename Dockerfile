FROM python:3.11-slim

WORKDIR /app

# Copying the necessary libraries 
COPY requirements.txt .

# Installing the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copying the python script
COPY baseApi.py .

# Running the Python script
CMD ["python", "baseApi.py"]
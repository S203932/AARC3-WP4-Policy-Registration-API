FROM python:3.11-slim

WORKDIR /app

# Copying the necessary libraries 
COPY requirements.txt .

# Installing the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copying the python script
COPY baseApi.py .

EXPOSE 8080

# Running the Python script
CMD ["gunicorn","-w", "4","-b", "0.0.0.0:8080", "baseApi:app"]
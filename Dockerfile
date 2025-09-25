FROM python:3.11-slim

WORKDIR /app

# Copying the necessary libraries 
COPY requirements.txt .


# REMOVE THIS LINE
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*


# Installing the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copying the python scripts
COPY baseApi.py .
COPY dbInit.py .
COPY tests/db_test.py .

# Copying the test data
COPY initializationDB.sql .


EXPOSE 8080

# Running the Python script
CMD ["gunicorn","-w", "4","-b", "0.0.0.0:8080", "baseApi:app"]
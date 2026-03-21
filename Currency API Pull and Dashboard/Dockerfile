# 1. Start with a lightweight Python image
FROM python:3.11-slim

# 2. Install 'libpq-dev' and 'gcc' so Python can talk to PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the internal folder where our code will live
WORKDIR /app

# 4. Copy the requirements file and install libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all your project files into the image
COPY . .

# 6. Tell Docker the Flask app runs on port 5000
EXPOSE 5000

# 7. The command to run your app
CMD ["python", "app.py"]

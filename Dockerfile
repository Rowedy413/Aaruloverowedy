# Base image with Python 3.10
FROM python:3.10-slim

# Set environment variable to buffer stdout/stderr
ENV PYTHONUNBUFFERED=1

# Working directory inside container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose port to match Flask app port (10000)
EXPOSE 10000

# Command to run Flask app with host=0.0.0.0 and port 10000
CMD ["python", "app.py"]

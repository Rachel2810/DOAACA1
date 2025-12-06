# -----------------------
# 1) Use official Python image
# -----------------------
FROM python:3.10-slim

# -----------------------
# 2) Install system dependencies required for scikit-learn & numpy
# -----------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    python3-dev \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# -----------------------
# 3) Set working directory inside container
# -----------------------
WORKDIR /app

# -----------------------
# 4) Copy requirements first (better caching)
# -----------------------
COPY requirements.txt .

# -----------------------
# 5) Install Python dependencies
# -----------------------
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------
# 6) Copy your entire project
# -----------------------
COPY . .

# -----------------------
# 7) Expose Flask port
# -----------------------
EXPOSE 5000

# -----------------------
# 8) Run Flask app
# -----------------------
CMD ["python", "app.py"]

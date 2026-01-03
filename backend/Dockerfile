FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system packages needed for building wheels if necessary
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential gcc g++ git libopenblas-dev liblapack-dev pkg-config \
	&& rm -rf /var/lib/apt/lists/*

# Upgrade packaging tools
RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt .
# Prefer binary wheels when available to avoid Cython compilation
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt gunicorn

COPY . .

EXPOSE 8000

# Use $PORT if provided by the host (Render sets this environment variable)
CMD ["sh", "-c", "gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}"]

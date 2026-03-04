# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install uv
RUN pip install uv

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy the rest of the project
COPY . .

# Create necessary directories
RUN mkdir -p prediction_output final_model templates

# Expose the app port
EXPOSE 8000

# Run the app using uv
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

And the `.dockerignore`:
```
.venv
__pycache__
*.pyc
*.pyo
*.pyd
.env
.git
.gitignore
*.egg-info
dist
build
.mypy_cache
.pytest_cache
FROM python:3.12.5-slim AS base-build

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files
COPY ./ecomm/pyproject.toml ./ecomm/poetry.lock ./

# Install the project's Python dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the application code
COPY ./ecomm/app /app/app
COPY ./ecomm/main.py ./ecomm/.env /app


# Expose the port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
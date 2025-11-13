# --- Stage 1: The Builder ---
# Use a complete Python image to install dependencies
FROM python:3.11-bookworm as builder

# Set the working directory for the virtual environment
WORKDIR /opt/venv

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install 'pip' tools
RUN pip install --upgrade pip

# Copy ONLY the production requirements file
COPY requirements.txt .

# Create a virtual environment and install dependencies in it
RUN python -m venv .
RUN . bin/activate && pip install --no-cache-dir -r requirements.txt


# --- Stage 2: The Final Image ---
# Start from a 'slim' (lightweight) image for production
FROM python:3.11-slim-bookworm as final

# Create a group and a non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set the application working directory
WORKDIR /home/appuser/app

# Copy the virtual environment with dependencies from the 'builder' stage
COPY --from=builder /opt/venv /opt/venv

# Copy our application code
# (Copy the entire 'app' folder to 'WORKDIR')
COPY app/ ./app

# Change ownership of all files to the non-root user
RUN chown -R appuser:appgroup /home/appuser/app /opt/venv

# Switch to the non-root user
USER appuser

# Expose port 8000 (where Uvicorn will run)
EXPOSE 8000

# Define the command to run the application
# 1. Activate the virtual environment
# 2. Run uvicorn
CMD ["/opt/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
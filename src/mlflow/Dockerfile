# Build an image from a Dockerfile | Command to use
# docker build -t <image_name>:<tag> <path_to_Dockerfile>
# eg: docker build -t my_image:latest .

# Runtime to use as a base image
ARG PYTHON_VERSION=3.12.7
FROM python:${PYTHON_VERSION}-slim



# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1


# Set the working directory in the container
WORKDIR /app


# Expose port
EXPOSE 8002

# Run commands in the container (used to install dependencies, set up the environment, etc.)
RUN apt-get update && apt-get install python3-pip -y

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


# Define environment variable
ENV PYTHONPATH=/app


# Start mlflow tracking server
CMD mlflow server --backend-store-uri $MLFLOW_TRACKING_URI --host $MLFLOW_HOST --port $MLFLOW_PORT
# Use the official NiceGUI image as the base image
FROM zauberzeug/nicegui:latest

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies using uv
# We use uv sync to ensure all dependencies from uv.lock are installed
RUN uv sync --frozen

# Expose the port that NiceGUI will run on
EXPOSE 8080

# Set environment variables for NiceGUI
ENV NICEGUI_HOST=0.0.0.0
ENV NICEGUI_PORT=8080
ENV NICEGUI_RELOAD=false
ENV PYTHONUNBUFFERED=1

# Start the application using uv run to ensure the correct environment
CMD ["uv", "run", "app/main.py"]

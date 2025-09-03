# Use Playwright base image (includes Chromium, Firefox, WebKit + deps)
FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Start Streamlit when container runs
CMD ["streamlit", "run", "webs2.py", "--server.port=8501", "--server.address=0.0.0.0"]

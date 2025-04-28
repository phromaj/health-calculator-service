# Use official Python runtime as a parent image
FROM python:3.13-alpine

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
# Copy requirements first for better layer caching
COPY requirements.txt /app/
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose port 5001 for the Flask app (corrected from 5000)
EXPOSE 5001

# Set environment variable for Flask (optional but good practice)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

# Run the Flask app using gunicorn (more production-ready than flask run)
# Install gunicorn first
RUN pip install --no-cache-dir gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]

# --- Original CMD kept for reference ---
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
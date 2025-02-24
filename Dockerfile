# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY bot/requirements.txt .

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 2005

# Copy the rest of the application code
COPY bot/. .

# Specify the command to run the bot
CMD ["python", "bot.py"]
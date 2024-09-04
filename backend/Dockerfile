# Use an official Python runtime as a parent image
FROM python:3.9.6

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code into the container at /app
COPY . .

# Expose port 5000 for the application
EXPOSE 5000

# Run the application
# CMD ["python", "main.py"]
CMD ["python", "mainWithDB.py"]

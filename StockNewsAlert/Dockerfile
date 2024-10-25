# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Get secrets from environment variables
ENV ALPHA_VANTAGE_API_KEY=$ALPHA-VANTAGE-API-KEY
ENV NEWS_API_KEY=$NEWS-API-KEY
ENV TWILIO_ACCOUNT_SID=$TWILIO-ACCOUNT-SID
ENV TWILIO_AUTH_TOKEN=$TWILIO-AUTH-TOKEN

# Run main.py when the container launches
CMD ["python", "main.py"]

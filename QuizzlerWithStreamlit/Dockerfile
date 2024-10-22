FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 (8501) available to the world outside this container
EXPOSE 8501

# Streamlit-specific commands
RUN mkdir ~/.streamlit && \
    cp config.toml ~/.streamlit/config.toml && \
    cp credentials.toml ~/.streamlit/credentials.toml

# Define the default command to run when the container starts
CMD ["streamlit", "run", "main.py"]

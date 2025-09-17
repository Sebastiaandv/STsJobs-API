FROM python:3.13-slim
 
# Creating and setting working dir
RUN mkdir /app
WORKDIR /app
 
# Set environment variables 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# Installing python packages
RUN pip install --upgrade pip 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Initializing container
COPY . .

RUN chmod +x start.sh

EXPOSE 8000
 
# Run server
ENTRYPOINT [ "./start.sh" ]
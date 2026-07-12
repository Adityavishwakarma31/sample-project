# Use pyhton for base image
FROM python:3.11-slim
# creating a working directory
WORKDIR /app
# copy main file from project
COPY app.py /app/
# copy requirments file
COPY requirements.txt /app/
# Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt
# Create environments
ENV DB_HOST=db \
    DB_NAME=mydatabase \
    DB_USER=postgres \
    DB_PASSWORD=postgres \
    DB_PORT=5432
# Expose port
EXPOSE 5000
# Run Command
CMD ["python","app.py"]

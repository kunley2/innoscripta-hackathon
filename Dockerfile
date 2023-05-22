FROM python:3.9.13 
# Image from dockerhub
EXPOSE 5000 
# Expose the port 8000 in which our application runs
RUN apt update
RUN pip install --upgrade pip
# Upgrade pip
WORKDIR /app 
# Make /app as a working directory in the container
COPY . .
# RUN pip install chromadb
RUN pip install -r requirements.txt 
CMD ["python", "main.py"]
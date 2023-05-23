FROM python:3.9.13 
# Image from dockerhub
EXPOSE 5000 
# Expose the port 5000 in which our application runs
RUN apt update
RUN pip install --upgrade pip
RUN pip install langchain 
RUN pip install openai 
RUN pip install chromadb
RUN pip install flask
RUN pip install tiktoken
RUN pip install bs4

# Upgrade pip
WORKDIR /app 
# Make /app as a working directory in the container
COPY . .
# RUN pip install chromadb
# RUN pip install -r requirements.txt 
CMD ["python", "main.py"]
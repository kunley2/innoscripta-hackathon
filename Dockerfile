FROM python:3.9.13 
# Image from dockerhub
# Expose the port 5000 in which our application runs
RUN apt update
RUN pip install --upgrade pip
RUN pip install langchain==0.0.177 
RUN pip install openai 
RUN pip install chromadb
RUN pip install flask
RUN pip install tiktoken
RUN pip install bs4
RUN pip install google-search-results
RUN pip install fastapi google-api-python-client

# RUN pip install gunicorn[gevent]

EXPOSE 8000 
# Upgrade pip
WORKDIR /app 
# Make /app as a working directory in the container
COPY . .
# RUN pip install -r requirements.txt 
CMD ["python", "main.py"]
# CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5000 wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info
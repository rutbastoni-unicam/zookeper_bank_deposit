FROM python:3.11-alpine

WORKDIR /app

RUN pip install kazoo

COPY client.py .

# client launched with no output buffering, otherwise you won't see output logs for never-ending scripts
CMD ["python", "-u", "client.py"]

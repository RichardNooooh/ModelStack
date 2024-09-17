FROM python:3.12.6
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/src
WORKDIR /app/src
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
# TODO setup environment variables for db

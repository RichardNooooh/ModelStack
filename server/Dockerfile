FROM python:3.12.6
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/src
WORKDIR /app/src
CMD ["fastapi", "run", "app.py", "--port", "80"]
# TODO setup environment variables for db

FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install psycopg2-binary
COPY . /code/

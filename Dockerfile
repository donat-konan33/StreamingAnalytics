FROM python:3.8.14-slim

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1
ENV PORT=5000

WORKDIR /app

COPY ./lwqueue ./lwqueue
COPY ./pyproject.toml  ./pyproject.toml
COPY ./poetry.lock  ./poetry.lock


RUN apt-get update \
    && apt-get -y upgrade \
    && pip3 install --no-cache-dir poetry==2.0.1 \
    && poetry install --only main \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE $PORT

ENTRYPOINT [ "poetry", "run" ]

#CMD ["sh", "-c", "python lwqueue/clickhouse_queries.py"]
#CMD ["python", "lwqueue/clickhouse_queries.py", "-P", "5000", "-H", "0.0.0.0", "--debug" ]
# for production ENTRYPOINT [ "python", "lwqueue/clickhouse_queries.py", "-P", "5000", "-H", "0.0.0.0" "--no-reloader" ]

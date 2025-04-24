FROM python:3.13

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false 

COPY app/poetry.lock app/pyproject.toml ./
RUN poetry install --no-root

COPY ./app ./opt/app
ENV PATH "${PATH}:/opt/app"
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"
WORKDIR /opt/app

EXPOSE 8000

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

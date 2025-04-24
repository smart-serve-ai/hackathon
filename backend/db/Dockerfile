FROM postgres:17

RUN apt-get update && apt-get upgrade -y

COPY ./init-db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh


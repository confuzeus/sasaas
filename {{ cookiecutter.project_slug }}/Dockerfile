FROM node:lts-bullseye-slim AS node

ARG DOCKER_BROWSERSYNC_PORT=3000

WORKDIR /app

EXPOSE $DOCKER_BROWSERSYNC_PORT

ENV PATH ./node_modules/.bin/:$PATH

COPY docker/node-entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

USER node

ENTRYPOINT ["entrypoint.sh"]

FROM python:3.10-slim-bullseye AS piptools

ARG DOCKER_UID=1000
ARG DOCKER_GID=1000

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev

WORKDIR /app/requirements

RUN addgroup --gid $DOCKER_GID python && \
    adduser --gid $DOCKER_GID --uid $DOCKER_UID --disabled-password \
     --gecos '' python

COPY docker/piptools-compile.sh /usr/local/bin/compile.sh

RUN chmod +x /usr/local/bin/compile.sh

USER python

RUN pip install --user pip-tools

ENV PATH /home/python/.local/bin:$PATH
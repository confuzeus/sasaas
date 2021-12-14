FROM node:lts-bullseye-slim AS node

ARG DOCKER_BROWSERSYNC_PORT=3000

WORKDIR /app

EXPOSE $DOCKER_BROWSERSYNC_PORT

ENV PATH ./node_modules/.bin/:$PATH

COPY docker/node-entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

USER node

ENTRYPOINT ["entrypoint.sh"]
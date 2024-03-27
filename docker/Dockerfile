FROM python:3.10-slim

ENV USR_LOCAL_BIN=/usr/local/bin \
    APP_DIR=/www
ENV PROJECT_ROOT=$APP_DIR/project

RUN mkdir -p $PROJECT_ROOT/

COPY ./docker/start_web.sh $USR_LOCAL_BIN/
COPY ./docker/entrypoint.sh $USR_LOCAL_BIN/
COPY ./docker/gunicorn.conf.py $PROJECT_ROOT/

WORKDIR $PROJECT_ROOT

RUN set -ex && \
    apt-get update && \
    apt-get install -y nano python3-dev default-libmysqlclient-dev build-essential pkg-config && \
    python -m pip install --upgrade --force pip && \
    pip install wheel pipenv && \
    apt-get autoremove

COPY ./Pipfile* $PROJECT_ROOT/

RUN pipenv install --system --deploy

ADD ./src $PROJECT_ROOT

ENTRYPOINT ["entrypoint.sh"]

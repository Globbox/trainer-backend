FROM python:3.10-slim

# Enviroment variables
ENV APP_ROOT=/www \
    USR_LOCAL_BIN=/usr/local/bin \
    PYTHONDONTWRITEBYTECODE=1
    PYTHONUNBUFFERED=1

# Install dependensis
RUN set -ex && \
    apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config && \
    python -m pip install --upgrade --force pip && \
    pip install wheel pipenv && \
    # Clear apt cache
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p $APP_ROOT/ && \
    mkdir -p $APP_ROOT/logs && \
    mkdir -p $APP_ROOT/static && \
    mkdir -p $APP_ROOT/media

COPY ./docker/prod/entrypoint.sh $USR_LOCAL_BIN/

RUN sed -i 's/\r//' $USR_LOCAL_BIN/entrypoint.sh && \
    chmod +x $USR_LOCAL_BIN/entrypoint.sh

WORKDIR $APP_ROOT

COPY ./Pipfile* $APP_ROOT/

RUN pipenv install --system --deploy --ignore-pipfile

COPY ./src $APP_ROOT

ENTRYPOINT ["entrypoint.sh"]
FROM python:3.10-slim

# Enviroment variables
ENV APP_ROOT=/www \
    PROJECT_ROOT=/www/backend \
    USR_LOCAL_BIN=/usr/local/bin \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependensis
RUN set -ex && \
    apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    ffmpeg \
    pkg-config && \
    python -m pip install --upgrade --force pip && \
    pip install wheel pipenv && \
    # Clear apt cache
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p $APP_ROOT/ && \
    mkdir -p $PROJECT_ROOT && \
    mkdir -p $APP_ROOT/logs && \
    mkdir -p $APP_ROOT/static && \
    mkdir -p $APP_ROOT/media

COPY ./docker/dev/entrypoint.sh $USR_LOCAL_BIN/

RUN sed -i 's/\r//' $USR_LOCAL_BIN/entrypoint.sh && \
    chmod +x $USR_LOCAL_BIN/entrypoint.sh

WORKDIR $PROJECT_ROOT

COPY ./Pipfile* $PROJECT_ROOT/

RUN pipenv install --system --deploy --ignore-pipfile

COPY ./src $PROJECT_ROOT

# # Create Non-Root user
# RUN groupadd -r appusergroup && \
#     useradd -r -g appusergroup \
#     --no-create-home \
#     appuser

# RUN chown -R appuser:appusergroup $APP_ROOT $USR_LOCAL_BIN && \
#     chmod -R u+rwx,g+rx,o-rwx $APP_ROOT

# USER appuser
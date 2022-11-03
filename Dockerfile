FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /code/
RUN mkdir /code/static/
RUN mkdir /code/media/
RUN mkdir /code/log/

WORKDIR /code/keyserver/

RUN apt update -y && apt install -y --no-install-recommends xmlsec1 libssl-dev libsasl2-dev
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python -

COPY pyproject.toml /code/
COPY poetry.lock /code/

RUN /etc/poetry/bin/poetry config virtualenvs.create false --local && /etc/poetry/bin/poetry install --only main

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY uwsgi.ini /code/
COPY keyserver /code/keyserver/

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

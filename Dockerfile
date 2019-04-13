FROM python:3.7
RUN apt-get update
RUN apt-get install -y libzbar0

RUN pip install poetry

WORKDIR /usr/src/app

COPY pyproject.toml /usr/src/app
COPY poetry.lock /usr/src/app

RUN poetry install --no-dev

COPY . /usr/src/app
RUN poetry install --no-dev

CMD ["poetry", "run", "pyroscript", "start_server", "--port", "8080", "--debug"]

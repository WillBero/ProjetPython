FROM python:3.10-slim

WORKDIR /app



RUN apt-get update && apt-get upgrade && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.4.2

COPY . .

ENV PATH="/root/.local/bin:$PATH"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/root/.local'

RUN poetry install --no-root

CMD [ "python3", "-m" , "flask", "run","--host=0.0.0.0"]

EXPOSE 5000

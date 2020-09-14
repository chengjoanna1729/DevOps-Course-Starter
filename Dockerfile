FROM python:3.8.5-buster as base

WORKDIR /src

RUN pip install poetry

COPY . /src/

RUN poetry install

EXPOSE 5000

FROM base as production
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

FROM base as development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]
FROM python:3.8.5-buster as base
WORKDIR /src
RUN pip install poetry \
    && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /src/
EXPOSE 5000

FROM base as production
RUN poetry install --no-root --no-dev
COPY . /src/
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0", "wsgi:app"]

FROM base as development
RUN poetry install
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]
FROM python:3.12-alpine as base

RUN python -m pip install poetry

WORKDIR /app

COPY manage.py ./manage.py
COPY pyproject.toml poetry.lock ./

COPY todo/ ./todo
COPY todolistprj/ ./todolistprj

RUN python -m poetry install


FROM base as production
CMD python mange.py runserver

FROM base as test
CMD python -m poetry run python manage.py test

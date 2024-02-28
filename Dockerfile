FROM python:3.12-slim

WORKDIR /.

COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY . .

CMD ["python", "manage.py", "migrate"]

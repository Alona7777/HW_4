FROM python:3.11-slim-bullseye

RUN pip install poetry==1.7.1

WORKDIR .

COPY pyproject.toml poetry.lock ./
COPY . .
RUN touch README.md

RUN poetry install

EXPOSE 3000

ENTRYPOINT ["python", "main.py"]

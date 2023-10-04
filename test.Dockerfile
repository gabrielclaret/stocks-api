FROM python:3.11-slim-bookworm

WORKDIR /api-tests

COPY api ./api
COPY tests ./tests
COPY requirements.txt requirements.txt
COPY requirements-tests.txt requirements-tests.txt
COPY .coveragerc .coveragerc

RUN pip install -r requirements.txt
RUN pip install -r requirements-tests.txt

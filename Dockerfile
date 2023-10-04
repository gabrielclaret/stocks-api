FROM python:3.11-slim-bookworm

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN mkdir api

COPY api api
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt

ENV TZ="UTC"

CMD python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT

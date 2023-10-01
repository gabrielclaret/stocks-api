FROM python:3.11-slim-bookworm

COPY infra infra

RUN pip install -r /infra/requirements.txt

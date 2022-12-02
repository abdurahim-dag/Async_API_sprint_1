FROM python:3.10 as base

WORKDIR /app

COPY requirements.txt .

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

ARG appuser
RUN useradd -U $appuser
USER $appuser

FROM base as prod

COPY . .

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

FROM base as dev

CMD [ "uvicorn", "main:app", "--reload"]

FROM python:3.10 as base

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ARG appuser
RUN useradd -U $appuser
USER $appuser

FROM base as prod

COPY ./src .

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]

FROM base as dev

CMD [ "uvicorn", "main:app", "--reload"]

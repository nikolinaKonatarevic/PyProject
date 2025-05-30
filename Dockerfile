FROM python:3.12-alpine AS builder

ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app

RUN apk add --no-cache bash util-linux gcc musl-dev linux-headers libpq libffi-dev

#Installing libraries
RUN pip install --upgrade pip poetry==1.8.3 && \
    apk add --no-cache netcat-openbsd

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry lock &&  \
    poetry install --no-root --all-extras --with dev,api


FROM python:3.12-alpine  as runtime

WORKDIR /app

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

#Creating a group and seting a user
RUN addgroup --gid 1000 appuser && \
    adduser appuser -DH -h /app -u 1000 -G appuser

#copy all dep
COPY src/ /app/src
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/bin /usr/bin
COPY --from=builder /usr/lib/lib* /usr/lib/
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY ./tests /app/tests

ENTRYPOINT ["sh", "/entrypoint.sh"]
FROM python:3.12-alpine AS builder

ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apk add --no-cache bash util-linux gcc musl-dev linux-headers libpq libffi-dev

# Installing libraries
RUN pip install --upgrade pip poetry==1.8.3 && \
    pip install fastapi uvicorn  && \
    apk add --no-cache netcat-openbsd

COPY poetry.lock pyproject.toml ./

FROM python:3.12-alpine  as runtime

WORKDIR /app

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

#Creating a group and seting a user
RUN addgroup --gid 1000 appuser && \
    adduser appuser -DH -h /app -u 1000 -G appuser

USER appuser

#copy all dep
COPY src/ /app/src
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/bin /usr/bin
COPY --from=builder /usr/lib/lib* /usr/lib/
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

ENTRYPOINT ["sh", "/entrypoint.sh"]

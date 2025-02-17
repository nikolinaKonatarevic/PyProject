FROM python:3.12-alpine AS builder

ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apk add --no-cache bash util-linux gcc musl-dev linux-headers libpq libffi-dev

# Installing libraries
RUN pip install --upgrade pip poetry==1.8.3
RUN pip install fastapi uvicorn
RUN apk add --no-cache netcat-openbsd

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry lock

RUN poetry install --no-dev

FROM python:3.12-alpine  as runtime

WORKDIR /app

RUN apk add --no-cache netcat-openbsd

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN addgroup --gid 1000 appuser && \
    adduser appuser -DH -h /app -u 1000 -G appuser

USER appuser

#copy all dep
COPY src/ /app/src
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/lib/lib* /usr/lib/
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

ENTRYPOINT ["sh", "/entrypoint.sh"]
#CMD ["python3", "src/main.py"]




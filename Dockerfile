FROM  python:3.7-alpine

WORKDIR /app

COPY requirements.txt ./
COPY Makefile ./

RUN apk add make zlib-dev jpeg-dev gcc musl-dev
RUN make develop
COPY . /app

RUN make migrate

ENTRYPOINT [ "python", "./manage.py", "runserver", "0.0.0.0:8080" ]

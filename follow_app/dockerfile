FROM python:3.11-alpine

ARG APP_NAME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_NAME}

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ${APP_NAME}

COPY ./scripts/entrypoint.sh /entrypoint
RUN chmod +x /entrypoint

COPY ./scripts/start.sh /start
RUN chmod +x /start

ENTRYPOINT [ "/entrypoint" ]
CMD ["/start"]
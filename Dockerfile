FROM python:3.5

EXPOSE 6000

ENV APP_DIR /usr/src/rovu-api

RUN mkdir $APP_DIR

WORKDIR $APP_DIR

COPY . $APP_DIR

RUN pip install -r requirements.txt && \
    chmod -R ug+rw $APP_DIR

ENTRYPOINT ["gunicorn"]

CMD ["rovu.app:create_app()", "-w", "4", "-b", "0.0.0.0:5050", "--worker-class", "meinheld.gmeinheld.MeinheldWorker", "--error-logfile", "-", "--access-logfile", "-"]

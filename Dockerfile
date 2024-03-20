FROM python:3.12-slim

ENV PIPENV_VENV_IN_PROJECT=1
ENV LANG=es_ES.UTF-8
ENV DEBUG=False

COPY --chmod=700 install-packages.sh .
RUN ./install-packages.sh

COPY --chmod=555 entrypoint.sh /entrypoint.sh
COPY app /app
RUN chown 65534:65534 -R /app
WORKDIR /app

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install --system --deploy

USER nobody
ENTRYPOINT [ "/entrypoint.sh" ]

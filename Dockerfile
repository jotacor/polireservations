FROM python:3.12

ENV PIPENV_VENV_IN_PROJECT=1
ENV GECKO_DRIVER=0.34.0
ENV LANG=es_ES.UTF-8
ENV DEBUG=False

COPY --chmod=700 install-packages.sh .
RUN ./install-packages.sh

RUN wget https://github.com/mozilla/geckodriver/releases/download/v${GECKO_DRIVER}/geckodriver-v${GECKO_DRIVER}-linux64.tar.gz && \
    tar -xvzf geckodriver-*.tar.gz && \
    rm geckodriver-*.tar.gz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin

COPY --chmod=555 entrypoint.sh /entrypoint.sh
COPY app /app
RUN chown 65534:65534 -R /app
WORKDIR /app

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install --system --deploy

USER nobody
ENTRYPOINT [ "/entrypoint.sh" ]
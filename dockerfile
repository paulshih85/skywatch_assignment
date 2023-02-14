FROM python:3.10.10
LABEL Maintainer="bohan.shih"

WORKDIR /usr/app/src
ENV VIRTUAL_ENV /usr/app/src
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH $VIRTUAL_ENV/bin:$PATH

COPY server.py .
COPY client ./client/
COPY execute.sh .env .
ENTRYPOINT ["bash", "execute.sh"]

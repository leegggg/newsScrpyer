FROM python:3.6-alpine
RUN apk add --update alpine-sdk
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD app /app
ADD conf /app/conf
ENV        SHELL=/bin/bash
CMD python /app/InternetScrpyer.py /app/conf/config.json
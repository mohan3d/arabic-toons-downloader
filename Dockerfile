FROM jrottenberg/ffmpeg:4.4-alpine

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /arabic-toons-downloader
COPY .  /arabic-toons-downloader

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "downloader.py"]
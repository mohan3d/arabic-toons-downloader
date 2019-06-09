FROM python:3.7-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev rtmpdump-dev

WORKDIR /arabic-toons-downloader
COPY .  /arabic-toons-downloader

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "downloader.py"]
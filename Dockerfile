FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install selenium

WORKDIR /workdir
COPY main.py .
COPY logger.py .
ENV PYTHONIOENCODING=utf-8
ENTRYPOINT [ "python3", "main.py" ]
FROM ubuntu:18.04
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /workdir
COPY main.py .
ENTRYPOINT [ "python3", "main.py" ]
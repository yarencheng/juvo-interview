FROM ubuntu:18.04
RUN apt-get update && apt-get install -y git python
RUN git clone https://github.com/novnc/noVNC.git
WORKDIR /noVNC
ENTRYPOINT ./utils/launch.sh --vnc selenium:5900 --listen 6080
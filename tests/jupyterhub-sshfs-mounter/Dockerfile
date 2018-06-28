FROM debian:latest
MAINTAINER Rasmus Munk <rasmus.munk@nbi.ku.dk>

RUN apt-get update && apt-get install -yq --no-install-recommends \
    python3-dev \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY main.py main.py
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/usr/bin/python3", "main.py"]
CMD ["--hub-url=http://127.0.0.1:8888", "--mount-url=/hub/mount", "--auth-url=/hub/login"]
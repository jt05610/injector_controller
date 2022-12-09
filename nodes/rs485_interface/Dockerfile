FROM ubuntu:22.04
COPY . /app

USER root
RUN apt-get update && apt-get -y install cmake

USER ${user}
WORKDIR $HOME


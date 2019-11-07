FROM ubuntu:18.04

RUN apt-get update && apt-get -y install curl firefox python3 python3-pip locales \
 && curl -L "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz" |tar zx -C /bin/
RUN echo "ja_JP UTF-8" > /etc/locale.gen && locale-gen
ENV LANG ja_JP.UTF-8
ADD . /src/
WORKDIR /src
RUN pip3 install -r requirements.txt



FROM python:3.6
LABEL maintainer="Alexander Drykov <SpamerSD@gmail.com>"
LABEL name="telegram-bot"
LABEL version="latest"

RUN apt-get update;\
    apt-get install -y \
        tor \
        python3-pip;


RUN pip3 install --upgrade pip \
    && pip3 install \
      pyTelegramBotAPI \
      beautifulsoup4 \
      requests \
      PySocks;

ARG TOKEN
ARG CHANNEL_NAME
ARG IMAP_SERVER
ARG IMAP_PORT
ARG IMAP_LOGIN
ARG IMAP_PASSWORD

RUN echo "# -*- coding: utf-8 -*-">>config.py; \
    echo "TOKEN="${token}>>config.py; \
    echo "CHANNEL_NAME="${CHANNEL_NAME}>>config.py; \
    echo "IMAP_SERVER="${IMAP_SERVER}>>config.py; \
    echo "IMAP_PORT="${IMAP_PORT}>>config.py; \ 
    echo "IMAP_LOGIN="${IMAP_LOGIN}>>config.py; \ 
    echo "IMAP_PASSWORD="${IMAP_PASSWORD}>>config.py;\
    echo "nameserver "${DNS_SERVER} > /etc/resolv.conf;    


RUN curl -O https://raw.githubusercontent.com/Spamersd/erepeater_bot/master/bot.py; \
    curl -O https://raw.githubusercontent.com/Spamersd/erepeater_bot/master/entrypoint.sh;    

CMD ["./entrypoint.sh"]

ENTRYPOINT ["bash"]

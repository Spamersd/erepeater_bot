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
      requests \
      PySocks;

RUN curl -O https://raw.githubusercontent.com/Spamersd/erepeater_bot/master/bot.py; \
    curl -O https://raw.githubusercontent.com/Spamersd/erepeater_bot/master/entrypoint.sh;    
COPY ./config.py  ./config.py

CMD ["./entrypoint.sh"]

ENTRYPOINT ["bash"]

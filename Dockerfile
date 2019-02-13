FROM python:3.6
LABEL developer="SpamerSD@gmail.com"

RUN apt-get update;\
    apt-get install -y tor;\
    apt-get install -y python3-pip;

RUN  pip install pytelegrambotapi;\
     curl -O https://raw.githubusercontent.com/Spamersd/erepeater_bot/master/bot.py;
COPY ./config.py  ./config.py
    
ENTRYPOINT python3 bot.py
